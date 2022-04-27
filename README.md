# music_generator
对音乐属性进行编码，使用lstm生成一段美妙的音乐

### 1. 运行方法

- 安装 music21,并配置环境变量

- 运行 preprocess.py
- 运行 train.py

> 如您想直接使用预训练的模型进行生成，请直接运行此步：
- 运行 melody_generator.py (如果你想根据一小段旋律来根据网络生成后面的旋律，只需更改"seed",数字表示单音，"_"表示持续时间，以16分音符作为持续单位)

### 2.数据集下载地址
https://kern.humdrum.org/cgi-bin/browse?l=essen/europa/deutschl

### 2.已生成的旋律

`mel.mid`          `mel1.mid`          `mel2.mid `

https://drive.google.com/file/d/18RC0ysImnqNiOHtrKBH9624xW2tlQc8M/view?usp=sharing

### 3.训练好的模型

https://drive.google.com/file/d/1zK4JJhLRghTdCVmDl0EfNT5Nwe8gLdZR/view?usp=sharing

