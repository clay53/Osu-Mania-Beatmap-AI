interval=50

badLabels=("0,0,1,2" "0,1,2,0" "0,2,0,1" "0,2,0,2" "0,2,1,0" "0,2,1,1" "1,0,0,2" "1,0,2,1" "1,1,2,0" "1,2,0,0" "2,0,1,1" "2,1,1,0" "0,2,2,0" "0,0,2,1")
# 0 1000 5000 30000 60000
backPeeks=(15000)
# 4000 32000 128000
trainingSteps=(8192000)

for backPeek in ${backPeeks[@]}
do
    dataTitle="i"$interval"bp"$backPeek
    echo $dataTitle

    # python makeData.py $backPeek
    # mkdir "./"$dataTitle
    # for badLabel in ${badLabels[@]}
    # do
    #     mv "./data/"$badLabel "./"$dataTitle"/"$badLabel
    # done
    # mv "./data" "./"$dataTitle"/data"
    
    cd ./tensorflow-for-poets-2
    for steps in ${trainingSteps[@]}
    do
        IMAGE_SIZE=224
        ARCHITECTURE="mobilenet_0.50_${IMAGE_SIZE}"
        python -m scripts.retrain --bottleneck_dir=tf_files/bottlenecks --model_dir=tf_files/models/"${ARCHITECTURE}" --summaries_dir=tf_files/training_summaries/"${ARCHITECTURE}" --output_graph=tf_files/retrained_graph.pb --output_labels=tf_files/retrained_labels.txt --architecture="${ARCHITECTURE}" --image_dir="../"$dataTitle"/data" --how_many_training_steps $steps
        python makeSong.py $backPeek
        
        cd "./tf_files"
        trainingTitle="s"$steps$dataTitle
        mkdir $trainingTitle
        mv "./bottlenecks" "./"$trainingTitle"/bottlenecks"
        mv "./training_summaries" "./"$trainingTitle"/training_summaries"
        mv "./retrained_graph.pb" "./"$trainingTitle"/retrained_graph.pb"
        mv "./retrained_labels.txt" "./"$trainingTitle"/retrained_labels.txt"
        mv "../../encoded.asu" "./"$trainingTitle"/encoded.asu"
        cd "../"
    done
    cd "../"
done