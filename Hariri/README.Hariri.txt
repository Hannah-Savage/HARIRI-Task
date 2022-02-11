README for the Fear Conditioning Task

*****************************************************************SUMMARY**************************************************************************



*****************************************************************TRIAL STRUCTURE******************************************************************

      [         instructions         ] ->
      ^                              ^
INSTRUCT_ONSET                   TASK_ONSET

    4s                                  32s                                 10s                                               4s
[fixation] ->                   [Face or Shape Block]                 -> [fixation] -> [Face or Shape Block] ->.........-> [fixation]
^                                                                        ^                                                 ^
FIXATION_ONSET                                                         FIXATION_ONSET                                    FIXATION_ONSET
           0.1s                      1.8s               0.1s        5s          5s        5s  
         [blank]   ->    [     Block Instruct     ] -> [blank] -> [Trial] -> [Trial] -> [Trial] ->
                         ^              ^ ^  ^    ^   
                    FACES_INSTRUCT   RESPONSE    FINAL_RESPONSE  (for completeness, button presses are recorded during the instruction slide, even though none are expected and they have no effect)
                    SHAPES_INSTRUCT

Trial
  0.1s           4.8s             0.1s
[blank] -> [Faces or Shapes] -> [blank] ->
           ^    ^  ^  ^    ^   
   FACES_ONSET  RESPONSE FINAL_RESPONSE
  SHAPES_ONSET


 

*****************************************************************INPUT DETAILS********************************************************************

EACH LINE CODES: one trial/instruct/fixation
COLUMN 1: Trial type (0->fixation, 1->faces instruct, 2->shapes instruct, 3->faces match, 4->shapes match)
COLUMN 2: top image, left image, right image
COLUMN 3: trial duration (will have 0.1s blanks at the beginning and end--so a 5s trial will have 4.8s of images shown)
COLUMN 4: correct response (0->none, 1->left, 2->right)
TRIAL ORDER IS: fixed


*****************************************************************OUTPUT DETAILS*******************************************************************

Trial Types:
0->fixation
1->faces instruct
2->shapes instruct
3->faces match
4->shapes match

INSTRUCT_ONSET (1)
response_time: not used
response: not used
result: not used

TASK_ONSET (2)
response_time: time between INSTRUCT_ONSET and TASK_ONSET
response: not used
result: not used

FIXATION_ONSET (3)
response_time: not used
response: (0 for none, 1 for left, 2 for right)
result: top_image left_image right_image

FACES_INSTRUCT (4)
response_time: not used
response: (0 for none, 1 for left, 2 for right)
result: top_image left_image right_image

SHAPES_INSTRUCT (5)
response_time: not used
response: (0 for none, 1 for left, 2 for right)
result: top_image left_image right_image

FACES_ONSET (6)
response_time: not used
response: correct response (0 for none, 1 for left, 2 for right)
result: top_image left_image right_image

SHAPES_ONSET (7)
response_time: not used
response: not used
result: top_image left_image right_image

RESPONSE (8)
response_time: time between FACES_ONSET or SHAPES_ONSET and RESPONSE
response: 1 for left, 2 for right, 0 for select button (should not be used, but just to see if they press the wrong button)
result: 0 for incorrect, 1 for correct

FINAL_RESPONSE (9)
response_time: time between FACES_ONSET or SHAPES_ONSET and the last RESPONSE
response: 1 for left, 2 for right, -1 for no response
result: -1 for no response, 0 for incorrect, 1 for correct


