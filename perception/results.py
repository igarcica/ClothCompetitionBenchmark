
import cv2
import csv

team = "IDLab-AIRO"
trial = 6
team_trials_path = "teams_trials/"+team+"/Perception/"
output_path="teams_trials/"+team+"/Perception/scoring/"
plain_img_path=team_trials_path+"trial_input_"+str(trial)+".png" # Plain image path to show results

#SAVE RESULTS TOTAL
team_corners_path = team_trials_path+"/trial_grasp_points_" + str(trial) + ".csv"
gt_corners_path = output_path+"trial"+str(trial)+"_gt.csv"
print(team_corners_path)
print(gt_corners_path)
gt_file = csv.reader(open(gt_corners_path))
team_file = csv.reader(open(team_corners_path))
gt_data = []
team_data = []
for rows in gt_file:
    gt_data.append(rows)
for rows in team_file:
    team_data.append(rows)

img = cv2.imread(plain_img_path)
for i in range(len(gt_data)):
    print(int(gt_data[i][0]))
    cv2.line(img, (int(gt_data[i][0]), int(gt_data[i][1])), (int(gt_data[i][2]), int(gt_data[i][3])), (255,127,0), 2)
    cv2.circle(img, (int(gt_data[i][0]), int(gt_data[i][1])), 3, (255,127,0), -1) #GT color?
for j in range(len(team_data)):
    print(int(team_data[j][0]))
    cv2.line(img, (int(team_data[j][0]), int(team_data[j][1])), (int(team_data[j][2]), int(team_data[j][3])), (0,0,255), 2)
    cv2.circle(img, (int(team_data[j][0]), int(team_data[j][1])), 3, (0,0,255), -1) #Team color? Red?

width = int(img.shape[1] * 300 / 100)
height = int(img.shape[0] * 300 / 100)
dim = (width, height)
img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
output_img_file=output_path+"trial"+str(trial)+"_results_all.png"
cv2.imwrite(output_img_file, img) # Save with trial number
cv2.imshow("Result image", img)
cv2.waitKey(0)
