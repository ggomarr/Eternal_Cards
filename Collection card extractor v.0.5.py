import pickle
import gzip
import pyautogui
import cv2
import os

screenshots_folder='./Screenshots/'
	# Where the collection screenshots are
collection_file='./my_collection.txt'
	# Where the collection will be saved to

library_local='./Libraries/'
    # Location of the pickled gzipped libraries with the artwork descriptors already calculated
    # that I prepared so that you don't have to.
library_root='card_library_set_'
    # Expected name of the library files - in case any other files rnd up in the same folder.

img_w,img_h=int(0.0479*pyautogui.size()[0]),int(0.1130*pyautogui.size()[1])
    # Size in pixels of the box used to extract features from.
    # Limited by either the resolution of your screen or that of the card artwork.
nfeatures=50
    # Number of features to extract from each box. 50 seems to work well.

# The parameters below define the places in the screenshots where we will extract image boxes and number owned diamonds from. Plenty of options would be available; I went for estimating:
# - The distance between cards (sep_x,sep_y), which when aplied to the position of the top left corner of the first image box (crd_x,crd_y) generates the boxes that will be used to extract owned card features (pos_lst)
# - The distance between the cards (the same sep_x,sep_y) and the horizontal distance between the ownership diamonds (sep_cnt), which when applied to the position of the center of the second diamond (the first one is a given - you always have at least one card of those present in the screenshots) of the top left card (cnt_x,cnt_y) generates the points to check if an ownership diamond is present (cnt_lst). This test is done against a cutoff of 100, but the actual values measured on the screenshots were 330 on yes-diamond and 15 on no-diamond

sep_x,sep_y=int(0.1218*pyautogui.size()[0]),int(0.3852*pyautogui.size()[1])
    # Represents the distances between equivalent positions of cards on the screenshot,
    # i.e., 'top left to top left' or 'center to center', or whatever
crd_x,crd_y=int(0.1730*pyautogui.size()[0]),int(0.2120*pyautogui.size()[1])
    # Represents the top left corner of the feature extraction box of the first card
pos_lst=[ (crd_x+n_x*sep_x,crd_y+n_y*sep_y,img_w,img_h)
          for n_y in range(2) for n_x in range(6)]
    # Represent the list of feature extraction boxes of the 12 cards

sep_cnt=int(0.013*pyautogui.size()[0])
    # Represents the horizontal distance between equivalent positions of diamods on the screenshot
    # i.e., 'top left to top left' or 'center to center', or whatever
cnt_x,cnt_y=int(0.1917*pyautogui.size()[0]),int(0.1463*pyautogui.size()[1])
    # Represents the center of the second ownership diamond of the first card
cnt_lst=[ [(cnt_x+n_x*sep_x+n_cnt*sep_cnt,cnt_y+n_y*sep_y) for n_cnt in range(3)]
          for n_y in range(2) for n_x in range(6)]
    # Represents the center of the second, third, and fourth diamonds of the 12 cards

owned_threshold=100
    # Threshold to determine whether at the point there is a yes-diamond or no-diamond.
    # The actual numbers are 330 for yes-diamond and 15 for no-diamond

def knn_match(des1, des2, nn_ratio=0.7):
    index_params = dict(algorithm = 0, trees = 5)
    search_params = dict(checks = 50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)
    good = []
    for m, n in matches:
        if m.distance < nn_ratio * n.distance:
            good.append(m)
    return good

def knn_clasif(good_matches):
    logprobs=[]
    best_template, highest_logprob = None, 0.0
    sum_good_matches = sum([len(gm) for gm in good_matches])
    for i, gm in enumerate(good_matches):
        logprob = len(gm)/sum_good_matches
        logprobs.append(logprob)
        if logprob > highest_logprob:
            highest_logprob = logprob
            best_template = i
    return best_template,logprobs

# The script extracts each card in each screenshot of the collection, compares its features with those of all the cards in the library, and finds the best match.
# 
# It can be made much faster by identifying additional features from the cards, such as power requirements profile, cost, or attack; these can then be used to narrow the search for the target card, which would also allow to reduce the size of the feature extraction boxes and the number of features being extracted from each box.
# 
# I also tried text extraction, but tesseract did not work well on the card names, at least not on my low resolution screenshots. That however does not mean it cannot be used to speed up the identification process, as long as the extracted gibberish is consistent.
# 
# To be explored.

library={}
for set_library in os.listdir(library_local):
    if library_root in set_library:
        with gzip.open(library_local+set_library,'rb') as library_file:
            library.update(pickle.load(library_file))

sift=cv2.xfeatures2d.SIFT_create(nfeatures=nfeatures)

list_cards=list(library)
for card in library:
    library[card]['owned']=0
errors=[]
tot=len(os.listdir(screenshots_folder))
cnt=0
for ss_file in sorted(os.listdir(screenshots_folder)):
    cnt=cnt+1
    print('[{:3d}/{:3d}] Processing file {}...'.format(cnt,tot,ss_file))
    if ss_file[-3:]=='png':
        screenshot=cv2.imread(screenshots_folder+ss_file)
        for i in range(12):
            l,t,w,h=pos_lst[i]
            target=cv2.resize(screenshot[t:t+h,l:l+w],(img_w,img_h))
            try:
                _,descriptors=sift.detectAndCompute(target,None)
                list_good_matches=[]
                for card in library:
                    list_good_matches.append(knn_match(library[card]['descriptors'],descriptors))
                best_match,probs=knn_clasif(list_good_matches)
                num_owned=1+sum([ screenshot[c[1],c[0],:].sum()>owned_threshold for c in cnt_lst[i]])
                print(12*' '+'- {} '.format(num_owned)+list_cards[best_match])
                library[list_cards[best_match]]['owned']=min(4,library[list_cards[best_match]]['owned']+num_owned)
            except:
                errors.append('[ERROR] Problem identifying card {:2d} in screenshot {}!'.format(i+1,ss_file))
                print(errors[-1])
                pass

my_collection=[]
for card in library:
    if library[card]['owned']>0:
        my_collection.append('{} {} (Set{} #{})'.format(library[card]['owned'],
                                                        card,
                                                        library[card]['set'],
                                                        library[card]['id']))
with open(collection_file,'w') as f:
    f.writelines([card+'\n' for card in my_collection])