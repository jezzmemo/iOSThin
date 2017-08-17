# iOSThin
我们在开发iOS的过程中，随着业务和功能的持续更新，人员的流动，第三方库的随意添加，App就是出于一个只有添加没有删除的，会导致App大小持续增加，所以在瘦身App是每个App必修的课程

# 如何解决

* 应用内资源

    * 用脚本来找到资源没有在程序中没有使用的资源,注意可能存在误伤的情况，记得让测试认真过下.
    
    * 网络下载资源，比如皮肤这种情况.
    
    * 压缩图片,js,html,audio,video.
    
    * On-Demand Resources
    
    iOS提供按需加载资源方案，iOS9以后才支持的,以tags来管理，除了Required的资源，其余都按需下载下来，这部分资源存储在App Store或者Cloud
    [具体文档在这里](https://developer.apple.com/library/content/documentation/FileManagement/Conceptual/On_Demand_Resources_Guide/index.html#//apple_ref/doc/uid/TP40015083-CH2-SW1)
    
* 优化编译选项

    `Strip Linked Product`
    
    `Deployment Postprocessing`
    
    `Symbols Hidden by Default`

    `Bitcode`
     
Bitcode类似于一个中间码，被上传到applestore之后，苹果会根据下载应用的用户的手机指令集类型生成只有该指令集的二进制，进行下发。从而达到精简安装包体积的目的,__需要注意的是如果打开这个开关，第三方库都需要支持，如果一个没开，就不能使用__

![bit code](https://lowlevelbits.org/img/bitcode-demystified/app_thinning.png)
    

* 代码优化

    1.建议工程不要swift和oc共存的情况，现在我们有很少量的swift代码，会导致app会几个swift依赖库，如果只有OC代码，可以介绍几M空间大小.
    
    2.空函数及默认实现的函数都可以删掉
    
    3.未使用类的扫描
    
    
    4.合并类似的第三方库，工程原来引用了Label就好几个，可以内部沟通选其中一个保留即可.
