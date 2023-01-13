
Windows 10 默认使用女性声音 Huihui 作为讲述人，如果使用男性 Kangkang 讲述人需要手工添加注册表信息

快捷方法：
导入 kangkang.reg 注册表信息

手动修改方法：
1. 使用 list_voices() 方法，获取当前 Windows 的讲述人列表信息；
2. 进入注册表，导出 Huihui 的注册表信息位置
3. 另存一份注册表，将其中的 Huihui 全部改成 Kangkang，并修改性别
4. 导入回注册表，并修改 VoicePath 中的 Huihui 为 Kangkang
5. 重新调用 list_voices() 方法，确认新的讲述人已加入