# iOS瘦身
我们在开发iOS的过程中，随着业务和功能的持续更新，人员的流动，第三方库的随意添加，App就是出于一个只有添加没有删除的，会导致App大小持续增加，所以在瘦身App是每个App必修的课程

## 应用内资源

> 用脚本来找到资源没有在程序中没有使用的资源,注意可能存在误伤的情况，记得让测试认真过下.
    
在这里我用一个[Python脚本](https://github.com/jezzmemo/iOSThin/blob/master/UnusedImage.py)来找出没有被用到的图片，然后删除掉，在使用之前需要配置下，资源目录和源码目录即可:
```python
#must set the imageasset path
imageSet = glob.glob('Resources/images.xcassets/*/*.imageset')

#option ignore the files
ignores = {r'image_\d+'}

# must set the source code path
sourcePath = ''
```
```sh
jezz$python UnusedImage.py
```

> 压缩图片,js,html,audio,video,plist，网络下载资源，比如皮肤这种情况.

- [ImageOptim](https://imageoptim.com/)无损压缩
- [Tinypng](https://tinypng.com/)在线压缩，收费的
    
> On-Demand Resources

iOS提供按需加载资源方案，iOS9以后才支持的,以tags来管理，除了Required的资源，其余都按需下载下来，这部分资源存储在App Store或者Cloud
[具体文档在这里](https://developer.apple.com/library/content/documentation/FileManagement/Conceptual/On_Demand_Resources_Guide/index.html#//apple_ref/doc/uid/TP40015083-CH2-SW1)

## 优化编译选项

> Strip Linked Product
    
> Deployment Postprocessing

我们工程这个默认是NO，我把这个设置成YES，对比了下，减少了0.1M左右，效果比较小
    
> Symbols Hidden by Default

> Asset Catalog Compiler

Optimizeation有两个选项，一个time,一个space，经过测试设置成space，减少0.1M左右

> 工程的Enable C++ Exceptions和Enable Objective-C Exceptions选项都设置为NO。手动管理异常。

因为在设置里都关了，如果有些源码用到了，在编译时候设置`-fexceptions`，这里如果用到了@try{}@catch{}的，就必须手动打开，因为工程里有@try的代码，所以没有来得及测试，不过在微信瘦身的文章的结论是关闭这个选项的效果是很大的，后面我有结果会跟大家分享的.

> Enable C++ Runtime Types 选项设置为NO

所有没有使用C++动态特性的lib库（搜索工程没有使用dynamic_cast关键字）

> Bitcode

Bitcode类似于一个中间码，被上传到applestore之后，苹果会根据下载应用的用户的手机指令集类型生成只有该指令集的二进制，进行下发。从而达到精简安装包体积的目的,__需要注意的是如果打开这个开关，第三方库都需要支持，如果一个没开，就不能使用__

![bit code](https://lowlevelbits.org/img/bitcode-demystified/app_thinning.png)
    

## 代码优化
> 分析Link Map文件

首先打开`Write Link Map File`,然后设置生成的路径，即可获取到Link Map.txt,这里就不讲内容部分了，网上讲解还是比较多的，如果有兴趣的朋友可以[查看这边](http://blog.cnbang.net/tech/2296/),在这里我用了一个现成的[Python脚本](https://github.com/jezzmemo/iOSThin/blob/master/ScanLinkMap.py)，会列出所有文件的方法的大小,还可以显示模块的大小，根据这些大小，你可以参考舍弃那些以及每次版本的对比，那个环节产生的空间最大.

> 建议工程不要swift和oc共存的情况

现在我们有很少量的swift代码，会导致app会几个swift依赖库，如果只有OC代码，可以减少几M空间大小.

> 建议不要使用XIB，有以下原因

* 容易发生冲突，修复成本高.
* 后期维护不方便，没有代码直观.
* 从瘦身的角度来说，增加了资源.


> 空函数及默认实现的函数都可以删掉

> 未使用类的扫描

> 合并类似的第三方库

公司规模大了以后，我们都知道进行拆分，比如有专门做基础模块的部分，有专门做业务的部门，两个部门之间如果只有对接，没有比较好的约束和沟通，就会导致大家各自做各自的，不关心有些组件是否重复，所以这个问题，一定要有一个给力的负责人，才能约束好各个部分，从而统一，尽量少的出现重复的情况.

## 总结

