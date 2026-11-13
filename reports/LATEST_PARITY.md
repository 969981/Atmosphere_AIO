# Independent rumla-style rebuild vs original

Experimental source assembly; NOT the original author's binary and NOT hardware tested.
The original .7z is never accessed by this builder.

| Comparison | Count |
| --- | ---: |
| reference_files | 277 |
| rebuilt_files | 103 |
| byte_identical | 96 |
| different_hash | 7 |
| missing_files | 174 |
| extra_files | 0 |
| exact_percent | 34.66 |

## Identical (96)

- atmosphere/config/override_config.ini
- atmosphere/config/stratosphere.ini
- atmosphere/config/system_settings.ini
- atmosphere/config_templates/boot2.flag
- atmosphere/config_templates/emummc-ER00/ER00/raw_based
- atmosphere/config_templates/emummc-ER00/emummc.ini
- atmosphere/config_templates/emummc-SD00/SD00/file_based
- atmosphere/config_templates/emummc-SD00/emummc.ini
- atmosphere/contents/00FF0000636C6BFF/exefs.nsp
- atmosphere/contents/00FF0000636C6BFF/toolbox.json
- atmosphere/contents/420000000007E51A/exefs.nsp
- atmosphere/contents/420000000007E51A/toolbox.json
- atmosphere/hbl.nsp
- atmosphere/hbl_html/accessible-urls/accessible-urls.txt
- atmosphere/hosts/default.txt
- atmosphere/hosts/emummc.txt
- atmosphere/hosts/sysmmc.txt
- atmosphere/package3
- atmosphere/reboot_payload.bin
- atmosphere/stratosphere.romfs
- bootloader/ini/more.ini
- bootloader/payloads/CommonProblemResolver.bin
- bootloader/payloads/DowngradeFixer.bin
- bootloader/payloads/Lockpick_RCM.bin
- bootloader/payloads/TegraExplorer.bin
- bootloader/payloads/Warmboot_Extractor.bin
- bootloader/payloads/fusee.bin
- bootloader/payloads/hwfly_toolbox.bin
- bootloader/sys/emummc.kipm
- bootloader/sys/l4t/bpmpfw.bin
- bootloader/sys/l4t/bpmpfw_b01.bin
- bootloader/sys/l4t/mtc_tbl_b01.bin
- bootloader/sys/l4t/sc7entry.bin
- bootloader/sys/l4t/sc7exit.bin
- bootloader/sys/l4t/sc7exit_b01.bin
- bootloader/sys/libsys_lp0.bso
- bootloader/sys/libsys_minerva.bso
- bootloader/sys/nyx.bin
- bootloader/sys/nyx.bin.en
- bootloader/sys/res.pak
- bootloader/sys/thk.bin
- bootloader/update.bin
- config/ovl-sysmodules/config.ini
- config/sphaira/config.ini
- config/status-monitor/config.ini
- config/sys-clk/config.ini
- config/tesla/config.ini
- config/ultrahand/config.ini
- config/ultrahand/lang/de.json
- config/ultrahand/lang/en.json
- config/ultrahand/lang/es.json
- config/ultrahand/lang/fr.json
- config/ultrahand/lang/it.json
- config/ultrahand/lang/ja.json
- config/ultrahand/lang/ko.json
- config/ultrahand/lang/nl.json
- config/ultrahand/lang/pl.json
- config/ultrahand/lang/pt.json
- config/ultrahand/lang/ru.json
- config/ultrahand/lang/uk.json
- config/ultrahand/lang/zh-cn.json
- config/ultrahand/lang/zh-tw.json
- config/ultrahand/overlays.ini
- exosphere.ini
- hbmenu.nro
- payload.bin
- switch/.overlays/EdiZon.ovl
- switch/.overlays/StatusMonitor.ovl
- switch/.overlays/lang/EdiZon/zh-Hans.json
- switch/.overlays/lang/EdiZon/zh-Hant.json
- switch/.overlays/lang/StatusMonitor/zh-Hans.json
- switch/.overlays/lang/StatusMonitor/zh-Hant.json
- switch/.overlays/lang/ovl-sysmodules/zh-Hans.json
- switch/.overlays/lang/ovl-sysmodules/zh-Hant.json
- switch/.overlays/lang/sys-clk/zh-Hans.json
- switch/.overlays/lang/sys-clk/zh-Hant.json
- switch/.overlays/ovl-sysmodules.ovl
- switch/.overlays/sys-clk.ovl
- switch/.packages/package.ini
- switch/Awoo-Installer/Awoo-Installer.nro
- switch/Checkpoint/Checkpoint.nro
- switch/DBI/dbi.config
- switch/DBI/translation.bin
- switch/DBI/translation.bin.cn
- switch/N-Xplorer.nro
- switch/NX-Activity-Log/NX-Activity-Log.nro
- switch/daybreak.nro
- switch/goldleaf/Goldleaf.nro
- switch/haze.nro
- switch/jksv/JKSV.nro
- switch/linkalho/linkalho.nro
- switch/sphaira/sphaira.nro
- switch/switch-time.nro
- switch/sys-clk-manager.nro
- switch/tinwoo/tinwoo.nro
- switch/wiliwili/wiliwili.nro

## Different SHA256 (7)

- bootloader/hekate_ipl.ini
- switch/.overlays/ovlmenu.ovl
- switch/DBI/DBI.nro
- switch/DeepSea-Toolbox/DeepSeaToolbox.nro
- switch/EdiZon/EdiZon.nro
- switch/reboot_to_payload.nro
- switch/tencent-switcher-gui.nro

## Missing (174)

- atmosphere/exefs_patches/es_patches/02DCD930D0A7462451E9973AB2022D697C77614B.ips
- atmosphere/exefs_patches/es_patches/03E4EB5556B98B327D1353E8AA2C7ADF2C544470.ips
- atmosphere/exefs_patches/es_patches/1114E9102F1EBCD1B0EAF19C927362CFCB8B5D2C.ips
- atmosphere/exefs_patches/es_patches/127904316C924326084288641825FE5DC259AF6B.ips
- atmosphere/exefs_patches/es_patches/34E95FF2929B5B767DCFD41D108AD927D2D7F5DC.ips
- atmosphere/exefs_patches/es_patches/39E7884F7DDEA9BE4FF9F7187898FACC466A080A.ips
- atmosphere/exefs_patches/es_patches/3B8BF56DBEC7225D2EE666B009C42C0DC4552010.ips
- atmosphere/exefs_patches/es_patches/4A258ADE9176A7F263532C2A4C30187A0B00C012.ips
- atmosphere/exefs_patches/es_patches/4FB9AFAED8A9093A3D88F6D61158B1C165F9444A.ips
- atmosphere/exefs_patches/es_patches/5AA09E1AF740A91D0F73ADFAE81A63E8AC0610D2.ips
- atmosphere/exefs_patches/es_patches/621351EB04199CF0B7A899896C451F2FD1B7A1CE.ips
- atmosphere/exefs_patches/es_patches/632246E2E62ECBD0D2CC8FD7D2AB15964CAFC462.ips
- atmosphere/exefs_patches/es_patches/702CD302FB341300BB1D69C96C7FC66FB80BE599.ips
- atmosphere/exefs_patches/es_patches/7135C20E752183914606CCE81293F24B738C3AEF.ips
- atmosphere/exefs_patches/es_patches/76935CA6235CA150D790D4DDF09CA3488AEF50D8.ips
- atmosphere/exefs_patches/es_patches/897C2CF2777B3A8845640C096933ACE61DD12272.ips
- atmosphere/exefs_patches/es_patches/8B2E677DE5991C87B35E84F7DDB8056F62D4582E.ips
- atmosphere/exefs_patches/es_patches/98BB737D9780E9FE3117981A77A09FF6756DBC2E.ips
- atmosphere/exefs_patches/es_patches/9C1B205852731D054B070529D320AD9649E7796C.ips
- atmosphere/exefs_patches/es_patches/A6E7D98BD335371E1B9A96F6241EA3E83B0C36F4.ips
- atmosphere/exefs_patches/es_patches/A9D9379170BA2E5490DCCE747A1C7286B7E4EF3D.ips
- atmosphere/exefs_patches/es_patches/C0BFC6518707AC975295A0B656A051DA885A9045.ips
- atmosphere/exefs_patches/es_patches/C6EB162251D3E1F4D7D1B20A8B807860C987B08A.ips
- atmosphere/exefs_patches/es_patches/CBF2D40A2210C4EE1137F80098DB776EAC7DDCC1.ips
- atmosphere/exefs_patches/es_patches/CF84DE5278AE823734DE630A098C6B1AEEF12894.ips
- atmosphere/exefs_patches/es_patches/CF8FB4F82D3E2D56720E1EDB14AB06543343E042.ips
- atmosphere/exefs_patches/es_patches/D0ECC9483E636AE19FE3E314DB41CB18019977D7.ips
- atmosphere/exefs_patches/es_patches/D2D2430244D162C9FAABE8C89A58C6E3962160F1.ips
- atmosphere/exefs_patches/es_patches/E581B1898637E5BC40DBC4AB8F0C6324447E05D1.ips
- atmosphere/exefs_patches/es_patches/F48ABC3EF41A0555800127D172C9B8D2C653243A.ips
- atmosphere/exefs_patches/es_patches/F65FBA401BAC3CDDEA4917DE22E8B426B3A6C3AD.ips
- atmosphere/exefs_patches/es_patches/F86D615F9FC6F0D16C3458BE58C64594DBDAB0DF.ips
- atmosphere/exefs_patches/es_patches/F92CFF283777465AFBCC6E160C10EFE7AADC4D3C.ips
- atmosphere/exefs_patches/es_patches/FBBDEC24489CB423E13226A8447BE27B7E7193B7.ips
- atmosphere/exefs_patches/nfim_ctest/0C4C2220D90155B139E254179D2D35244B32C9C1.ips
- atmosphere/exefs_patches/nfim_ctest/184A3F5734F456D0718FA35D15D8410A9BDFC537.ips
- atmosphere/exefs_patches/nfim_ctest/1A7811338EBD94E04D0475C078809CB182AF739A.ips
- atmosphere/exefs_patches/nfim_ctest/1BD31ABF1E3E607CA79B29CF7D7B10758FF93FA0.ips
- atmosphere/exefs_patches/nfim_ctest/22A811D739A648F3967343DAFEB7353C2EA942AB.ips
- atmosphere/exefs_patches/nfim_ctest/2C3E24F46D131685B361FEE1F0570B985095E034.ips
- atmosphere/exefs_patches/nfim_ctest/2E29B2674BF76671333C96F3272B1CA6CECF8477.ips
- atmosphere/exefs_patches/nfim_ctest/38774C42DFCB8B9D7AA61550D6AF7D335472556C.ips
- atmosphere/exefs_patches/nfim_ctest/3AED90979B380C6415F975F5B784BEA2B4730E8C.ips
- atmosphere/exefs_patches/nfim_ctest/43F10952AE80CFADC39A0BF59EA4E552EF4A4528.ips
- atmosphere/exefs_patches/nfim_ctest/440F71259BCA1E97EA3663CBD6EC9315951F9E96.ips
- atmosphere/exefs_patches/nfim_ctest/523D2C6E08D9BE4B512AD20AA5628B7BB06D73C2.ips
- atmosphere/exefs_patches/nfim_ctest/5835E2DADB4DD570DD811ABF521FA91AC3C7B717.ips
- atmosphere/exefs_patches/nfim_ctest/5DA461C7B6CAE6B88EDF4F914F7CBCF0943B10BB.ips
- atmosphere/exefs_patches/nfim_ctest/69E25CDEEED5C6520AC2AC8E5EAE01CD8FC46E40.ips
- atmosphere/exefs_patches/nfim_ctest/6F02D68B1DCD2AFFBAED14B5933F81F3C327E537.ips
- atmosphere/exefs_patches/nfim_ctest/7A43F840337C28D453718843608EEFF78AFD460B.ips
- atmosphere/exefs_patches/nfim_ctest/7DF07326B6B50CA37F19C1C44F9458406C536B30.ips
- atmosphere/exefs_patches/nfim_ctest/881206E6B5078EFC4E2C30D7B33E33AD266538C6.ips
- atmosphere/exefs_patches/nfim_ctest/88E62489B53EB7AF4D1A2B5ED21D2EFEB581BE16.ips
- atmosphere/exefs_patches/nfim_ctest/8CB532EA199207191F04CE3DDECEC854C7CF07D6.ips
- atmosphere/exefs_patches/nfim_ctest/929014BFCFE462FD76B2BB3454FB304F63C73AC2.ips
- atmosphere/exefs_patches/nfim_ctest/9C72C47F0310F7C9F487047D8EB42DBB96882088.ips
- atmosphere/exefs_patches/nfim_ctest/A188828ADF447425D97901462EBF732D2E29BC4E.ips
- atmosphere/exefs_patches/nfim_ctest/A2C3AEE4E5A954908BEBAEDEA2010095E9E521B2.ips
- atmosphere/exefs_patches/nfim_ctest/A85F50FBA10E06A3EBA3D3FACB9E075B218C7D6D.ips
- atmosphere/exefs_patches/nfim_ctest/AD32FB6D8F36668C586E538E32576A8D6A3931C0.ips
- atmosphere/exefs_patches/nfim_ctest/B206E5323EA13A4F1A4BE29FDAA0FB4341866DEB.ips
- atmosphere/exefs_patches/nfim_ctest/B6966381A806655B718F1BF11DB5FF836E3085F7.ips
- atmosphere/exefs_patches/nfim_ctest/BA91B5A61E423F51FB83B2C9E6C153CC5AE27DCB.ips
- atmosphere/exefs_patches/nfim_ctest/D47D1506009B340829CD545B2A3F3AA7881FBADA.ips
- atmosphere/exefs_patches/nfim_ctest/D82361E0D66DC01AFA3B5116532E5E1ED569C578.ips
- atmosphere/exefs_patches/nfim_ctest/E6BFDADD5C69E17D43B7C67E2B2EE8B2E50C8E1F.ips
- atmosphere/exefs_patches/nfim_ctest/FD53CB863709DFFEC19C0889F61D4C424AFFD4ED.ips
- atmosphere/exefs_patches/nim-prodinfo-blank-fix/0CDDAED25D1DEF356243866F7657B4026993996A.ips
- atmosphere/exefs_patches/nim-prodinfo-blank-fix/412CA954A47280118C72280EFAEAC33F490793B6.ips
- atmosphere/exefs_patches/nim-prodinfo-blank-fix/4240898DA430050F363C4F740C40514AE244AFFD.ips
- atmosphere/exefs_patches/nim-prodinfo-blank-fix/5CFAC5752420D8B8933A9A4D83FD58AAC3CEE112.ips
- atmosphere/exefs_patches/nim-prodinfo-blank-fix/7A0ECCE9375DC38BA907EE7F9F4BD6046075AF96.ips
- atmosphere/exefs_patches/nim-prodinfo-blank-fix/9A576C1A8BE653CD24C88A8C239DADA3E1EF73F8.ips
- atmosphere/exefs_patches/nim-prodinfo-blank-fix/B469C48D7102CC0BA09AC447249E43F9BAAC245E.ips
- atmosphere/exefs_patches/nim-prodinfo-blank-fix/C14BC0AD5027F6B6B49A5A6B2D52D5E8306EE1D2.ips
- atmosphere/exefs_patches/nim-prodinfo-blank-fix/C54A1B3EB06FF3F5DCCBAC1AEFD5CA5459A2A6E6.ips
- atmosphere/exefs_patches/nim-prodinfo-blank-fix/CC269DEA7E3AE16FAA39215F5A1CEF5C82FA1C00.ips
- atmosphere/exefs_patches/nim-prodinfo-blank-fix/DAEEEF46027BA6E83688C05C396E6C6B17F29001.ips
- atmosphere/kip_patches/fs_patches/01ED6B874C1FEF414B23E2B52FD775E560721BB93FD716D4EA66479CC23A4831.ips
- atmosphere/kip_patches/fs_patches/02D5ABAAFD20C8B0633AA0DBAEE0377EF526CE6AD2AC6F2CAD7180CE69E74311.ips
- atmosphere/kip_patches/fs_patches/06E90719595A010C6246FF70946F10FB367A00BBD8B7D8D1F25CCE0B458D7E89.ips
- atmosphere/kip_patches/fs_patches/073099D7C6AD7D8983BC7ADD932BE3D1243193792E0920955DBC17F5794FDE28.ips
- atmosphere/kip_patches/fs_patches/0BA15BB304B505633B6DA6B2C6E991B6A06EBAFB3378DF02BF6B494075976F06.ips
- atmosphere/kip_patches/fs_patches/0D7005627B07767C0B963F9AFFDDE56628A27116CFC4D8B2AF42BDEEBF97205B.ips
- atmosphere/kip_patches/fs_patches/10B2D81605488599DF2242CB6BAC2DF1E2BCAB3BC19DC5CD63DB6FAEC0947097.ips
- atmosphere/kip_patches/fs_patches/160D3E104EAD6176991B8AE7AFA2B78BC5879FC07BE88A4FC9E16812971BC161.ips
- atmosphere/kip_patches/fs_patches/1E2C64B1CCE27824999B9DC2276701696C9569CBC607501D65CC1386CE485B65.ips
- atmosphere/kip_patches/fs_patches/204CBA86DE08446A4ED2B6925C1981675D1FE81C1CA71D5B8B6DD76396C8B5F7.ips
- atmosphere/kip_patches/fs_patches/27073BF0A1B8CE6108EEC562D654669ECC5AE576F42D2A9FF6424C623B98E8D8.ips
- atmosphere/kip_patches/fs_patches/2ADBE97E9B5F41779EC95FFE2699C93305D6A69D465CF597D67465CD69BACCE8.ips
- atmosphere/kip_patches/fs_patches/2CCE659CEC536A8E4D91F3BE4B74BED302613F1E442581FD863708E39112DB50.ips
- atmosphere/kip_patches/fs_patches/330553F6B5FB55C4C2D7B736240276B3EAD664DA79826FA936F99803B6C28F3B.ips
- atmosphere/kip_patches/fs_patches/34383EE7999263403BA7577817404E72A2BDE0B14A7B309DD26E685A94D6E145.ips
- atmosphere/kip_patches/fs_patches/34C0D9ED6AD1873DCD02F1C12AFA20546D033EFB1D8EB9B7A8E5ABAB71F39F43.ips
- atmosphere/kip_patches/fs_patches/39EE1F1E0EA7325DD105C1BABE90F306A5AA5DEC70024D4F9461F94C8E0206AE.ips
- atmosphere/kip_patches/fs_patches/3A574D436186191D1788EB2C0F076B11737132EBB1484CF906B6A8EB3B1BF459.ips
- atmosphere/kip_patches/fs_patches/3EEBD9B7BCD1B5E0BCC2007D6514F7A4845A1F42AAD795573FD2865DADE1C5E0.ips
- atmosphere/kip_patches/fs_patches/468740761E193EB758794688F1D9F762CBA1185ADDAD4EC3C479EC8FBFEC31DD.ips
- atmosphere/kip_patches/fs_patches/47410710654FA43FE8B6D13B769C1EAF08309DCA55F3B2416970DC0B6D397231.ips
- atmosphere/kip_patches/fs_patches/51EBFA9CCF66C09EC796C069C6C6D03C01D504CC0B17F4FAA919446E7E9DB107.ips
- atmosphere/kip_patches/fs_patches/536D938469FE73BE3C76DA0333B289C0ED29F10C2A8AFDFF8E466142C4277359.ips
- atmosphere/kip_patches/fs_patches/549B0F8D6F72C4E9F3FD1F19EACE4A5A1DA2D5C393F74224F8BC09DE4AAA4217.ips
- atmosphere/kip_patches/fs_patches/562517A192C3C8F0BFF7B2D73F7949988D480361A90CBFC1FDE113329E7B2D30.ips
- atmosphere/kip_patches/fs_patches/56E856566C38D8BEA79A70FF6F9756804CFF57907E2EAC7BD8E9C1FC1C7B96CE.ips
- atmosphere/kip_patches/fs_patches/57397C063F10B6313F4D837653CCC371BE2158BF6DD889326648D5C83D50CECF.ips
- atmosphere/kip_patches/fs_patches/62C65EFD9ABF7C434275AA99BE0A0D9A222E89805044A6C04ADAB26D2AA1AA5E.ips
- atmosphere/kip_patches/fs_patches/6354969E60A7977B5A3C0E25EF39DEC1D84AC43E4F2BE16B3521A4FB4D6D0548.ips
- atmosphere/kip_patches/fs_patches/6B09B67B29C020246DC34F5A04F5D3090215C46F37BD079442977A85B8243BA5.ips
- atmosphere/kip_patches/fs_patches/6E2BD9BAA3B910F1D236A3304534603795DAA62AA9F2807328A29CAEF908DF4B.ips
- atmosphere/kip_patches/fs_patches/763827EE9C207E5BA99AE5BDC872DFCFB69D8F1261D80A60F3AC25AC9C90C230.ips
- atmosphere/kip_patches/fs_patches/76F87402C9387C0F0A2FAB1B45CEBB93E3E9695C7CFD390F00509B1204101C24.ips
- atmosphere/kip_patches/fs_patches/795F5A5EB0C6779EF2D5763E0052B3FB605C796869FE268F0C58714861EFCAEC.ips
- atmosphere/kip_patches/fs_patches/7B902837F20027497415E2AD51534E6EF83C8FC1E242271C429CDC8F3E66CB47.ips
- atmosphere/kip_patches/fs_patches/7C951376E5C12DF85FA6A9F46F6957A4B1271C1F8201B99735D8DF152E7913F1.ips
- atmosphere/kip_patches/fs_patches/7D200547178A836A24993B002AFD83D0B662AA7177E935C04C36EAC21BAC24AA.ips
- atmosphere/kip_patches/fs_patches/8096AF7C6A35AA8271F3916995413B0B64CE03BD9BBFEB26F2B3E01C5427C69E.ips
- atmosphere/kip_patches/fs_patches/817EA2B0B702C1F37EC5E0A7A61F745440422037DAA3537CEF4E856C40273F78.ips
- atmosphere/kip_patches/fs_patches/887AC150806C75CCC40DA0AA98CC09B3E468E6C78F315F927FBEDD91B16DE27A.ips
- atmosphere/kip_patches/fs_patches/91BA65A21C1D50AEF6E6B535B491A36CD1B2DFB2DA2F0AB4A93F03097BB894E0.ips
- atmosphere/kip_patches/fs_patches/981C57E7F02F70F7BCDE753181D901A62A2452B04F5C5FB86500A2172CC44641.ips
- atmosphere/kip_patches/fs_patches/A339F01C95BFA768DE461DA745130E932531C2DF986E3BC649A0B89CED0A1CC7.ips
- atmosphere/kip_patches/fs_patches/A51AA4926C41875905D1DA2FE9788FC849F8699F9FB5CE42EBD7B89FD5D08B8B.ips
- atmosphere/kip_patches/fs_patches/A6F27AD9AC7C73AD419B63B23E785A0CD7AA9DC1A63C57D10049423DE7B77E2C.ips
- atmosphere/kip_patches/fs_patches/A86DA5E87EF1097B23DAB5B4DBBAEFE780310AE643D319D6A7A149B9688651A5.ips
- atmosphere/kip_patches/fs_patches/A952B657ADF9C2BA1434BA9B8B86F3317D20659A8AC8510D8ECF4CE1BD7593E2.ips
- atmosphere/kip_patches/fs_patches/AF1DBDC782983CBDCF446D3BB7DB1F5408552974C63BC2DA42DD0A28EAF3E5DD.ips
- atmosphere/kip_patches/fs_patches/B2F5176B3548364D079A29B141A23B06AFFF5A98055576D5F337A621C0233CE3.ips
- atmosphere/kip_patches/fs_patches/B4CAE1F24965D92ED24EBE9E97F609C363834471BF18CA375CB6A1DEB77755EA.ips
- atmosphere/kip_patches/fs_patches/B5E7A64C6F5C4FE319C36FD7D642F75B0159771671F73082448ACE30BD6BAE89.ips
- atmosphere/kip_patches/fs_patches/B7A29739B7EDDEFCF37665FD06EF1F37B9F7ED3A34C88C85858E27738121C5C4.ips
- atmosphere/kip_patches/fs_patches/C86762BE19A51FA0C737AE921A816846605A64739523B4894F847BBED59E31EA.ips
- atmosphere/kip_patches/fs_patches/CD7BBE18D6130B28F62F19FA7945535B6829EFE64EF4AAF0DF8DA19885FE4A9A.ips
- atmosphere/kip_patches/fs_patches/CE3ECBA2F2F062F575F8F360842B32B432340DD2C7590CDEFC03E51B844AE805.ips
- atmosphere/kip_patches/fs_patches/CFAB450C2C539DA947D0A12A9DE10911FA539A348B7C3D64CE9BA74D9E0355DE.ips
- atmosphere/kip_patches/fs_patches/D0D4491814B562AF61ABD52E4BF0989405AF741A5C7C033AB3EB0EC8680AD98F.ips
- atmosphere/kip_patches/fs_patches/D44528295B4192BAAA42DF13488322AC0DD4714C57FA11154707762CF23E7687.ips
- atmosphere/kip_patches/fs_patches/D488D1F29217355C22ABDA773FDEA582B13D475B74BCB02B998C66AB1B3E4309.ips
- atmosphere/kip_patches/fs_patches/D5A5BF36640C49EA1D6BC5826772EEDFC11FD8626146B388E5E59322719B6AF7.ips
- atmosphere/kip_patches/fs_patches/D94C6815F8F50A2067C841311CA88982824A2A79B86DFC58F91509760F317BB6.ips
- atmosphere/kip_patches/fs_patches/DBD85FCACC193DA83051C664E6452D32FD4F7922E5E29A281695B578347F8161.ips
- atmosphere/kip_patches/fs_patches/DBD941C0C53C52CCF7202C84D8E0F78013A3684D8AB5D128096674A8F7755B3D.ips
- atmosphere/kip_patches/fs_patches/DC2A084996BB3C010035FCF196F940597E0B8EBFF2AC701F34F9997CCB531CDE.ips
- atmosphere/kip_patches/fs_patches/DE9FDDA4085DD5FE68DCB20B41095BB4010856AF280201552F38273B44CECD6F.ips
- atmosphere/kip_patches/fs_patches/E1E8D3D6A2FE0B102CC79F8310EEEF66E5D14BCA2ED73454455FD87C615EEDC0.ips
- atmosphere/kip_patches/fs_patches/E399156E844EB0AA3CC5152979961C879F5E90696C1224A1BBE0FF1BCDBFD7DC.ips
- atmosphere/kip_patches/fs_patches/E76692DFAA0420E9FDD68E436316181814CBD72E915E153174332C6BEAA41FC3.ips
- atmosphere/kip_patches/fs_patches/ED34B450584A5B43150CFF94D6A7C49F6B7F4C649B7CC6A0D8A0BB316EB52B76.ips
- atmosphere/kip_patches/fs_patches/EDA87868A4490750DD5ABA6BA758FC1545945A874A42AC124D92944C6560FE9F.ips
- atmosphere/kip_patches/fs_patches/EE0F4BAC6D1FFC4BB5ADCBD12455B24E4EF924A3DB5F9158792F57FA11DA83A1.ips
- atmosphere/kip_patches/fs_patches/EE4B3012A68402255043E718CDC247C4D88F17A7BDC566FDA54D7EB702B0751C.ips
- atmosphere/kip_patches/fs_patches/F196D144D04445B6E7497CB6405B7FC305B54F961024BF432575296E4D52BC99.ips
- atmosphere/kip_patches/fs_patches/FB0B68DB2403D119A2D058741781AED1330F493F1065CC62B7CB42252AF4AC9B.ips
- atmosphere/kip_patches/fs_patches/FDAF163288E1080549189EC8CAF29D1E14335021739AC0A7353460108A5B2411.ips
- atmosphere/kip_patches/loader_patches/82F95A5AC7FA67CDEABFB885183E27C9C46554708CEBAA23A3F48D35D85A1513.ips
- boot.dat
- bootloader/bootlogo.bmp
- bootloader/patches.ini
- bootloader/payloads/picofly_toolbox.bin
- bootloader/res/auto.bmp
- bootloader/res/emucfw.bmp
- bootloader/res/lakka.bmp
- bootloader/res/syscfw.bmp
- bootloader/res/sysofw.bmp
- bootloader/res/ubuntu.bmp
- hbmenu.nsp
- sdloader.enc
- warmboot_mariko/wb_13.bin
- warmboot_mariko/wb_14.bin
- warmboot_mariko/wb_15.bin
- warmboot_mariko/wb_16.bin
- warmboot_mariko/wb_17.bin
- warmboot_mariko/wb_18.bin
- warmboot_mariko/wb_19.bin

## Extra (0)


## Download or extraction failures

- None

## Still unmapped

- 155 IPS patch files: source-specific verified build not yet available
- 7 warmboot_mariko/wb_*.bin: hardware firmware dependent, cannot assume safe redistribution
- custom bootlogo and icon BMP files: upstream origin/licensing not mapped
- SX boot.dat/sdloader.enc: source not mapped
- hbmenu.nsp universal forwarder: trusted source not mapped
- picofly toolbox: exact asset not mapped

Researched text configs applied: 46
