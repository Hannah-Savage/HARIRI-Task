
import os, random
from psychopy import visual, core, event, data, gui, sound


#taken from the top of TrialsfmriHaririBlock.ini
image_mapping = [None, 'blank.bmp',	'Cross.bmp',	'mform.bmp',	'memotion.bmp',	'circle.bmp',	'horizontal.bmp',	'vertical.bmp',	'anger1cm.bmp',
    'anger2cm.bmp',	'anger3cf.bmp',	'anger4cf.bmp',	'anger5jm.bmp',	'anger6jm.bmp',	'anger7jf.bmp',	'anger8jf.bmp',	'fear1cm.bmp',	
    'fear2cm.bmp',	'fear3cf.bmp',	'fear4cf.bmp',	'fear5jm.bmp',	'fear6jm.bmp',	'fear7jf.bmp',	'fear8jf.bmp',	'happy1cm.bmp',	'happy2cm.bmp',	
    'happy3cf.bmp',	'happy4cf.bmp',	'happy5jm.bmp',	'happy6jm.bmp',	'happy7jf.bmp',	'happy8jf.bmp']


def convert_one(filename):
    original = open(filename, 'r')

    output = open('T1000_HARI_Schedule' + filename + '.csv', 'w')
    output.write('TrialTypes (0->fixation; 1->faces instruct; 2->shapes instruct; 3->faces match; 4->shapes match),Stimuli (0->top; 1->left; 2->right), Durations, Correct Response (0->none; 1->left; 2->right)\n')

    current_trialtype = 0 #will keep track of trial type
    for line in original:
        tokens = line.split()
        #0 not used
        #1 top image (also implicitly specifies trial type)
        #2 left image
        #3 right image
        #4 correct response
        #5 not used (100ms blank at the beginning of trial)
        #6 not used (duration of trial minus 200ms)
        #7 trial length
        if tokens[1] == '2':
            trial_type = '0'
        elif tokens[1] == '3':
            trial_type = '2'
        elif tokens[1] == '4':
            trial_type = '1'
        elif int(tokens[1]) > 4 and int(tokens[1]) < 8:
            trial_type = '4'
        elif int(tokens[1]) > 7:
            trial_type = '3'
        else:
            print 'Unknown Trial Token: ' + tokens[1]
            core.quit()
        duration = int(tokens[7]) / 1000
        output.write(trial_type + ',' + 'media/' + image_mapping[int(tokens[1])] + ' ' + 'media/' + image_mapping[int(tokens[2])] + ' ' + 'media/' + image_mapping[int(tokens[3])] + ',' + str(duration) + ',' + tokens[4] + '\n')
        
    output.close()
convert_one('TrialsfmriHaririBlock.ini')
