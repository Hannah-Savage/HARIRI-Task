
import StimToolLib, os, random, operator
from psychopy import visual, core, event, data, gui, sound, prefs

#Hariri faces task

class GlobalVars:
    #This class will contain all module specific global variables
    #This way, all of the variables that need to be accessed in several functions don't need to be passed in as parameters
    #It also avoids needing to declare every global variable global at the beginning of every function that wants to use it
    def __init__(self):
        self.win = None #the window where everything is drawn
        self.clock = None #global clock used for timing
        self.x = None #X fixation stimulus
        self.output = None #The output file
        self.msg = None
        self.ideal_trial_start = None #ideal time the current trial started
        self.trial = None #trial number
        self.trial_type = None #current trial type
        self.x_coords = [0, -330, 330] #x coords for the top, left, and right images
        self.y_coords = [186, -174, -174] #y coords for the top, left, and right images

event_types = {'INSTRUCT_ONSET':1,
    'TASK_ONSET':2,
    'FIXATION_ONSET':3, 
    'FACES_INSTRUCT':4,
    'SHAPES_INSTRUCT':5,
    'FACES_ONSET':6, 
    'SHAPES_ONSET':7,
    'RESPONSE':8,
    'FINAL_RESPONSE':9,
    'TASK_END':StimToolLib.TASK_END}

trial_type_mapping = {'0':'FIXATION_ONSET',
    '1':'FACES_INSTRUCT',
    '2':'SHAPES_INSTRUCT',
    '3':'FACES_ONSET',
    '4':'SHAPES_ONSET'}
    
            
def do_one_trial(trial_type, top_image, left_image, right_image, duration, correct_response):
    
    #wait for 100ms at the beginning of a trial
    StimToolLib.just_wait(g.clock, g.ideal_trial_start + 0.1)
    #set the three images to draw every frame--will only flip the frame when the subjct makes/changes a response
    top_image.draw()
    left_image.draw()
    right_image.draw()
    #show images and record responses
    g.win.flip()
    image_onset_time = g.clock.getTime()
    image_string = top_image._imName + ' ' + left_image._imName + ' ' + right_image._imName
    StimToolLib.mark_event(g.output, g.trial, g.trial_type, event_types[trial_type_mapping[trial_type]], image_onset_time, 'NA', correct_response, image_string, g.session_params['signal_parallel'], g.session_params['parallel_port_address'])
    #clear pressed keys so that a very early press is not counted
    event.getKeys([g.session_params['left'], g.session_params['right'], g.session_params['select']])
    
    correct = '-1'
    last_response_time = -1
    last_response = -1
    while g.clock.getTime() < g.ideal_trial_start + duration - 0.1: #show image(s) for trial length minus 200ms (100 at the beginning, 100 at the end)
        StimToolLib.check_for_esc()
        key = event.getKeys([g.session_params['left'], g.session_params['right'], g.session_params['select']])
        if key:
            now = g.clock.getTime()
            if key[0] == g.session_params['left']: #record every response 
                last_response_time = now
                last_response = '1'
                if correct_response == '1':
                    correct = 1
                else:
                    correct = 0
                StimToolLib.mark_event(g.output, g.trial, g.trial_type, event_types['RESPONSE'], now, now - image_onset_time, last_response, correct, g.session_params['signal_parallel'], g.session_params['parallel_port_address'])
                if trial_type == '3' or trial_type == '4':
                    #only draw the selection box and redraw images during shape/face matching trials
                    top_image.draw()
                    left_image.draw()
                    right_image.draw()
                    g.left_box.draw()
                    g.win.flip()
            if key[0] == g.session_params['right']:
                last_response_time = now
                last_response = '2'
                if correct_response == '2':
                    correct = 1
                else:
                    correct = 0
                StimToolLib.mark_event(g.output, g.trial, g.trial_type, event_types['RESPONSE'], now, now - image_onset_time, last_response, correct, g.session_params['signal_parallel'], g.session_params['parallel_port_address'])
                if trial_type == '3' or trial_type == '4':
                    #only draw the selection box and redraw images during shape/face matching trials
                    top_image.draw()
                    left_image.draw()
                    right_image.draw()
                    g.right_box.draw()
                    g.win.flip()
            if key[0] == g.session_params['select']: #record if they press the select button--but don't draw the box
                StimToolLib.mark_event(g.output, g.trial, g.trial_type, event_types['RESPONSE'], now, now - image_onset_time, 0, 'NA', g.session_params['signal_parallel'], g.session_params['parallel_port_address'])
        StimToolLib.short_wait()
    #hide all of the image--should be blank for the last 100ms of each trial
    #wait until the end of the trial--should be another 100ms
    g.win.flip() #blank the screen
    if last_response_time > 0:#compute response time--will be -1 for trials with no response
        rt = last_response_time - image_onset_time
    else:
        rt = -1
    StimToolLib.mark_event(g.output, g.trial, g.trial_type, event_types['FINAL_RESPONSE'], last_response_time, rt, last_response, correct, g.session_params['signal_parallel'], g.session_params['parallel_port_address'])
    StimToolLib.just_wait(g.clock, g.ideal_trial_start + duration)
    g.ideal_trial_start = g.ideal_trial_start + duration

def set_image_locations(tops, lefts, rights):
    for i in tops:
        i.setPos([g.x_coords[0], g.y_coords[0]])
    for i in lefts:
        i.setPos([g.x_coords[1], g.y_coords[1]])
    for i in rights:
        i.setPos([g.x_coords[2], g.y_coords[2]])
        
def run(session_params, run_params):
    global g
    g = GlobalVars()
    g.session_params = session_params
    g.run_params = StimToolLib.get_var_dict_from_file(os.path.dirname(__file__) + '/HARI.Default.params', {})
    g.run_params.update(run_params)
    try:
        run_try()
        #StimToolLib.mark_event(g.output, 'NA', 'NA', event_types['TASK_END'], g.clock.getTime(), 'NA', 'NA', 'NA', g.session_params['signal_parallel'], g.session_params['parallel_port_address'])
        g.status = 0
    except StimToolLib.QuitException as q:
        g.status = -1
        
    StimToolLib.task_end(g)
    return g.status
    
def run_try():  
    
    param_filename = os.path.dirname(__file__) + '/data/' + g.session_params['SID'] + '_HARI.params'
    cs_order = StimToolLib.get_var_from_file(param_filename, 'order') #read counterbalance param from file, or pick it and put one and put it in the dialogue box
    schedules = [f for f in os.listdir(os.path.dirname(__file__)) if f.endswith('.schedule')]
    if not g.session_params['auto_advance']:
        myDlg = gui.Dlg(title="HARI")
        myDlg.addField('Run Number', choices=schedules, initial=str(g.run_params['run']))
        myDlg.show()  # show dialog and wait for OK or Cancel
        if myDlg.OK:  # then the user pressed OK
            thisInfo = myDlg.data
        else:
            print('QUIT!')
            return -1#the user hit cancel so exit 

        g.run_params['run'] = thisInfo[0]

    StimToolLib.general_setup(g)    
    
    
    schedule_file = os.path.join(os.path.dirname(__file__), g.run_params['run'])
    #param_file = os.path.join(os.path.dirname(__file__),'T1000_FC_Schedule' + str(g.run_params['run']) + '.csv')
    trial_types,images,durations,correct_responses = StimToolLib.read_trial_structure(schedule_file, g.win, g.msg)
    #pull out the relevent list parts (due to the flexibility to have multiple values in most of the input columns)
    top_images = images[0]
    left_images = images[1]
    right_images = images[2]
    durations = durations[0]
    correct_responses = correct_responses[0]
    
    #put the images where they need to go
    set_image_locations(top_images, left_images, right_images)

    
    start_time = data.getDateStr()
    
    param_file = g.run_params['run'][0:-9] + '.params' #every .schedule file can (probably should) have a .params file associated with it to specify running parameters (including part of the output filename)
    StimToolLib.get_var_dict_from_file(os.path.join(os.path.dirname(__file__), param_file), g.run_params)
    g.prefix = StimToolLib.generate_prefix(g)
    fileName = os.path.join(g.prefix + '.csv')
    g.output = open(fileName, 'w')
    
    sorted_events = sorted(event_types.items(), key=lambda item: item[1])
    g.output.write('Administrator:,' + g.session_params['admin_id'] + ',Original File Name:,' + fileName + ',Time:,' + start_time + ',Parameter File:,' +  param_file + ',Event Codes:,' + str(sorted_events) + ',Trial Types are coded as follows: (0->fixation; 1->faces instruct; 2->shapes instruct; 3->faces match; 4->shapes match)\n')
    g.output.write('trial_number,trial_type,event_code,absolute_time,response_time,response,result\n')
    
    g.border = visual.ImageStim(g.win, image=os.path.join(os.path.dirname(__file__),  'media','RedFrame.gif'), units='pix', mask=os.path.join(os.path.dirname(__file__),  'media/frame_mask.gif'))
    g.left_box = visual.ImageStim(g.win, image=os.path.join(os.path.dirname(__file__),  'media','RedFrame.gif'), units='pix', pos=[g.x_coords[1], g.y_coords[1]], mask=os.path.join(os.path.dirname(__file__),  'media/frame_mask.gif'))
    g.right_box = visual.ImageStim(g.win, image=os.path.join(os.path.dirname(__file__),  'media','RedFrame.gif'), units='pix', pos=[g.x_coords[2], g.y_coords[2]], mask=os.path.join(os.path.dirname(__file__),  'media/frame_mask.gif'))
    
    StimToolLib.task_start(StimToolLib.HARIRI_CODE, g)
    instruct_start_time = g.clock.getTime()
    StimToolLib.mark_event(g.output, 'NA', 'NA', event_types['INSTRUCT_ONSET'], instruct_start_time, 'NA', 'NA', 'NA', g.session_params['signal_parallel'], g.session_params['parallel_port_address'])
    #StimToolLib.show_title(g.win, g.title)
    StimToolLib.run_instructions(os.path.join(os.path.dirname(__file__), 'media', 'instructions', g.run_params['instruction_schedule']), g)


    g.trial = 0
    if g.session_params['scan']:
        StimToolLib.wait_scan_start(g.win)
    else:
        StimToolLib.wait_start(g.win)
    instruct_end_time = g.clock.getTime()
    StimToolLib.mark_event(g.output, 'NA', 'NA', event_types['TASK_ONSET'], instruct_end_time, instruct_end_time - instruct_start_time, 'NA', 'NA', g.session_params['signal_parallel'], g.session_params['parallel_port_address'])

    g.ideal_trial_start = instruct_end_time
    g.win.setColor([1,1,1])
    g.win.flip()
    g.win.flip()
    

    for t_type in trial_types:
        g.trial_type = t_type
        do_one_trial(t_type, top_images[g.trial], left_images[g.trial], right_images[g.trial], durations[g.trial], correct_responses[g.trial])
        g.trial = g.trial + 1
        
        
    #StimToolLib.just_wait(g.clock, g.clock.getTime() + 1) #wait 1 second so the total task length is an even number of seconds and ends on a TR
    
    
  
 


