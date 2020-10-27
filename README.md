# AI cup
## Download frozen_inference_graph.pb
[link](https://drive.google.com/file/d/1Qx4WuBlvWXoBokFa4xLycHr4hXf9GTyI/view?usp=sharing) 放到 out_graph_dir/saved_model_6000steps/

## CPU GPU設定
在 detect.py 第43行
* 有GPU 
```
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
```
* 沒GPU
```
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
```


## 執行 detect
-i 為要偵測的圖片資料夾, -o 為要輸出的圖片資料夾
```
python detect.py -i Dev/ -o Result/
```

