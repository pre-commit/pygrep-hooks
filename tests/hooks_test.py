import re

import pytest
from pre_commit.clientlib import load_manifest
from pre_commit.constants import MANIFEST_FILE

HOOKS = {h['id']: re.compile(h['entry']) for h in load_manifest(MANIFEST_FILE)}


@pytest.mark.parametrize(
    's',
    (
        'x = 1 # type: ignore_me',
        'x = 1  # type: int',
        'x = 1  # type int',
        'x = 1  # type: int  # noqa',
    ),
)
def test_python_use_type_annotations_positive(s):
    assert HOOKS['python-use-type-annotations'].search(s)


@pytest.mark.parametrize(
    's',
    (
        'x = 1',
        'x = 1  # type:ignore',
        'x = 1  # type: ignore',
        'x = 1  # type:  ignore',
        'x = 1  # type: ignore # noqa',
        'x = 1  # type: ignore  # noqa',
    ),
)
def test_python_use_type_annotations_negative(s):
    assert not HOOKS['python-use-type-annotations'].search(s)


@pytest.mark.parametrize(
    's',
    (
        '# noqa',
        '# NOQA',
        '# noqa:F401',
        '# noqa:F401,W203',
    ),
)
def test_python_check_blanket_noqa_positive(s):
    assert HOOKS['python-check-blanket-noqa'].search(s)


@pytest.mark.parametrize(
    's',
    (
        'x = 1',
        '# noqa: F401',
        '# noqa: F401, W203',
    ),
)
def test_python_check_blanket_noqa_negative(s):
    assert not HOOKS['python-check-blanket-noqa'].search(s)


@pytest.mark.parametrize(
    's',
    (
        'assert my_mock.not_called()',
        'assert my_mock.called_once_with()',
        'my_mock.assert_not_called',
        'my_mock.assert_called',
        'my_mock.assert_called_once_with',
        'my_mock.assert_called_once_with# noqa',
        'MyMock.assert_called_once_with',
    ),
)
def test_python_check_mock_methods_positive(s):
    assert HOOKS['python-check-mock-methods'].search(s)


@pytest.mark.parametrize(
    's',
    (
        'assert my_mock.call_count == 1',
        'assert my_mock.called',
        'my_mock.assert_not_called()',
        'my_mock.assert_called()',
        'my_mock.assert_called_once_with()',
        '"""like :meth:`Mock.assert_called_once_with`"""',
        '"""like :meth:`MagicMock.assert_called_once_with`"""',
    ),
)
def test_python_check_mock_methods_negative(s):
    assert not HOOKS['python-check-mock-methods'].search(s)


def test_python_noeval_positive():
    assert HOOKS['python-no-eval'].search('eval("3 + 4")')


def test_python_noeval_negative():
    assert not HOOKS['python-no-eval'].search('literal_eval("{1: 2}")')


@pytest.mark.parametrize(
    's',
    (
        'log.warn("this is deprecated")',
    ),
)
def test_python_no_log_warn_positive(s):
    assert HOOKS['python-no-log-warn'].search(s)


@pytest.mark.parametrize(
    's',
    (
        "warnings.warn('this is ok')",
        'log.warning("this is ok")',
        'from warnings import warn',
        'warn("by itself is also ok")',
    ),
)
def test_python_no_log_warn_negative(s):
    assert not HOOKS['python-no-log-warn'].search(s)

@pytest.mark.parametrize(
    's',
    (
        "`[code]`",
        'i like `_kitty`',
        # Fuzzy value generate using:
        # https://www.browserling.com/tools/text-from-regex
        r"`X?j/omL7zX.htrPM+=RWvew)P,-Bod2?.Le)J@y^^2<{3)<\eu$Sh>BD03ox][Mu*[)+RAX;&w;1*Q{<$m%p@b!ja`:",
        r"`2T{&j8:hGXH;NW[e7c0xv-Ysv69BCmgk?l/YJtU,_<@6|;Mps|8ZB&yt'|KPkaKT'6:E:h;h=k|V%zRr.Q>gJgRh`,",
        r"`#Dt#h`5",
        r" `HHWZ6)(~-JOKk.UI&_!?|_hZq~[qfZ@]A],*Y`u",
        r"`pj~yO|^,m1= 3{),r$/0b^IjI*-4]hcKAtpE2f,0x=0=@~bl-|T*&e6Ix&e`",
        r" `Qva8uO%$$n]JL7i`",
        r"`P\$O@1P-&?Z\@/r5)oynb.UJ;_i6R9qRiz$>[bh6#eYU,>O\qQe'8`d",
        r"`U8XnDf[Z-ee;&2FB7F0 :2g&Uc6fI,jH6:-?h9/9?K&3BV_Hi?'}Cd8\-0e+(`",
        r" `w^CrB\BblRKj({4UH|nfnRz[X 126<vY-y5$Q8GX5gf)0\"$;T@vs)e/Q/b0=BzF(zBvrv36>}WN`M",
        r" `}:0bU+\ar3hAS,m~.5tPW!SF~}eMv?6CwL63Ev\b?$ws2?\gY.[;3x1`",
        r" `M0s1.t:xl[!i.9dtanXVfGzc$k#tQ-}'~s=q*H+:m@G`x",
        r" `HgWb5ucIk7E-gk[EXX6}]HmYIx52E3\"+Cb~J0VR?{w`",
        r"`ek|Zx}+n,+3I5Z>HB-}T13'Md+WJf2rCg9^xI\oOA5GdWCYM(Yq7F:nfWu&K`I",
        r" `>|xt,PlkN8~y^d&!'TOAn:AI6CrBFVLO4E6B0nTrq'z8]l$PZMuP=?P6Pk+`",
        r" `<f4Xs05Mm&T;E~k*%N8d3Z,-JG\`,",
        r"`o_-3L#]=!5<mm8,waeU%'C<3=46J:m|cU@h%@Y 8~6tbYQSnspjMxkvV345m/{=nrzB`F",
        r"`p)OE/{F\"YV9gbbHU|}~3r{Ar2fcm}b#`",
        r" `_Vy}y(%cfM+d/TQW68fv6jMDGvHu,~kHkRyC<\"L$=<Py& SJNT]=[12Kf~C>9UTX'e*}y HP'HM`",
        r"`&X'!]Rb(MHy63t&z/6eXk~?I$e7$~121I5Q9Ke5Uhx-\"r\6^%aXy}Z1)}$2zjSS!szOE]~SkG? Ktla`",
        r"`6okMgx;?:dEaGu-OQQ_BQjD;>vWkFl`",
        r"`B,uuwaD*Y2X8'W-{p@,6b4kAI!TVR|j,77J1s,/Teg\6A^.Ds,UK%pY4!]DOG9YjuR:;NxS_\*|vo\"lgu=t/E0qGBLJ`>",
        r"`wC\-3\"sr~S]Gr.g(fzrzE.We[u^K[f9{g;Q{FH4X[/o8Pg>~v/4x#~p':emxb:(p;B'M{PT8XSC%$k<\"QA'0r1'`f",
        r"`SesiTt/g$~4%E-9t:X9-J;lo9FX~wD.+~)Zd#eLlGC3#Xq(\"vp{XtE)*\"ZC8>eK KpjiQ:[H !96yxMsn%7e`",
        r"`}0egN[vH)-jy/7W,L]UOT0BI|[jfq`@",
        r"`[Dc=_ h<_1!sh5}?h:r6z7gUZVk8&Jn\4 D_kO(YwY3_$Bmpu6u`",
        r"`:UuS`^",
        r" `3KsS|_f#8_lJUO)M>,%}@Y9n9g.cF%;Y(O*v;P/{p]eGFon5>)}Q[7jl_gAJ9^Bh:5n$FGJX+`:",
        r"`wGzVm<@E~_Xv$?=Hu<>>HvD2NZk ]A4`",
        r" `&zh&4xKM6ob6:skfThWJh=\k{yl`#",
        r"`accW&K85-y1pC&W.l5C&Sz@rm+Pktt>rgdLv}D8zGRbV9Uv$}JIIh])/&U~9m]Wu\FOUjnX=7!k@j`v",
        r" `&1v>XmyNazVji=E+zG[]\"FiB O^xpXugp\"z4yL?$L'k1Gy7;dngjGJKOYbIaVk]lF|||*T5!E4Y[`v",
        r" `+O`",
        r"`g+kBs*_;F{3-&\JgR##p_y3,w]B8#Oe}l}^G<k_;e4m3+b`",
        r"`\tN>*%,]w@2DVLAWi>\"ogT,_k\#]<J^y;\"wk2$e,Lg8'_?DfyEGj+(PY1m6 p*+u<zS7Tr-_$1vDpF2ix5 d3\"sf8kGG,W`u",
        r" `jh,y'BSSFS:30n[,Eg^E}b^Y'Sst{I=A 8RO.jT@8!^t2&GQI~<\" h?|X-I`P",
        r"`x\"I%n<_[St8`'",
        r"`}c^|#dP&WBt^LXEg ]/.K}F^n2u;._|T@0%X8^y_u1K\&r2+W`1",
        r"`NPq]8328#'X\"#+\"eV:1K~;f|4~CiPr+~MuWpxjeA~~`",
        r"`G4rsCG72D!P6u'h|.q>J_NxXNiSrw}P u;({9d8r\"mcU{O|5bxMLJNcVLzW5]a'&p^i`",
        r" `gpNvqxMcJ@(gerPvp%ux\pyg'hY]-rTP8QQyXw^$'ri\"F> yU{Maq8tKG.P:Z8\D*`",
        r"`}eM'f<.X/j9PvYQNap? 'XeC2gl-gTr0Zi4*)O=R^GG\"L+RXI*V4v1p(.+x7+'( (s1v$u<\h\"`",
        r"`Wn|~fg]}^XT XJ>1Dy&2dLuNr:%alclh@wa3cd~7);%F8aI]`-",
        r" `Zda6#/Fnq8+.^t^\'~UudMeG3<:~`",
        r" `='Qo{_Q\>a/bu_]<TwAlpBoA+2R-\"GO\"]!\"X{4{w679}KK4j02[2;y`s",
        r" `Y]hl+c}(>I'^pK\"MgYid` ",
        r"`~+A_Gu'GJ<Ss]|[H?aYH|u!GwMzn)Qe\Bq?[1C5/R Z\#!}u'z\":q/%Db#?X4Xp!roL!Yv`",
        r"`0ln%L({H>2EmD]2-WCbf:SpJpsg:wQL;L9;jO[A6HmvZryDC7m\mg*(M#r#Q)M`",
        r"`a7>LXSf)h|t8zkD:q$y`",
        r" `;=TXj&E!H\"H&?mJWoHadx70j_5\"UcE#H8)5CcVt%Bs$h51/bV\L|Hbux*'\"tu>[:6U6h7zqRT<#HN7+z=O}i.e`",
        r"`S9G UFT6&0|zvs!H>#v#VKLF$;+$p)`",
        r"`MTOfdXe[UX<B\*o-RQB_]++Tmv7WL%JM[9nDkgOTN,\"#+HJTo-vo>etG#`x",
        r"`bP>DWOA3b Is:RaP9)1FRAo0{3@vyt'HD84D/!bfRCj?;$BCtm27<=_9\|fsY{~uv~oMW:M;%OjA;Tau6#n.`",
        r" `aWQFB9qsacFDa!V\{&`",
        r" `U{%g-iB]T8`",
        r" `I{)g\"<09#qc,q !j >,zNkrA0IX[KFFEU;{73K;+CXjp9~^LbB!zl2('tjsy&#\"l()`;",
        r"`eduef.sA?7,dB(), 6SF;VS%R{$A\"anN@0?$6SoC^3&VUfp]USvx,no?)&;NKWYgudNc+BW)Y0\"*HB+5{mg@f(&R`",
        r"`4uk4\"V6JI@}mSqP|xiG0y357eh\"SJ=w%{?):tov~EjhS9h;j%PN'ywZ)Xr*\"@FW,hf9Av|Ab^yZ2^\icR+C`~",
        r"`Co(DQ9&?AW,/R)_@q,>sAn\nB19Ney<(j#(=jubI`+",
        r"`J{4rvS%10AMM_^nkf|ippK^&?rvF_oBW}`]",
        r" `{}l=qt0!W#m:gP$qF#/[;nLBE/fx#&#0$w;}~Ur[%Ze<8VT-+33Sh]6:*^}w\"5m\%1G0`A",
        r"` /dFm?k9lC'U;-DZ;ltgWSUJ3CH(V. 6 \p?vZ-Ln@IQ.>&nIFx,aP+(pNjSDf:s3CblBJzob>%Ua.Js`0",
        r"`PbW8bYacjkh;|L/y^W fca{Da4:G'et?%bX(1z?`",
        r"`]rHa{^-*1g!aH$tJ'!5~V6HMU!)c_\"wCuPBQtLY+u>tktX%.u7F5;14>J`",
        r"`\"UgYN@5K0'x]\"vRVDi*cnUOaIu f=o0#ii-MmXOk;d4:n5z6X\"}uba9'?Epf\"gfJIf7yc <V5<yzq%rl%R\3`5",
        r"`Q6wBD}MJ*(\"d(~8+Ka<%+%lj>[9O}`-",
        r" `J/GmI^pI}$v>,WpRfu5pYS-:|^tONqjsA[.e.4l^{%/ubuGpVzVkuR#UgJdC3`!",
        r"`&B%aYM1(IDu;'>+Nbloz?5Ls-7=9z:vrtIi7y.z(J2-D]o0^o`b",
        r"`(^;[ U3hvu}}&?Y=^=6rxt|y|6WX,{#)pwO{X9!`",
        r"`nEC8OnuMjv/J$&)r^`",
        r" `Tm\_BZoJt\eR^*<WL'0_kI>=L#i%V7L$FmzYDQ_>4\"W)FAZ69i-^*KLxnsX.K1JWYW4v*iH,^wV|gO2rd]bNmlxADPTf K0g`7",
        r"`W0]AZp@I9V^)kv]Q+>E,i6~Sz>49Wa)#9LRg9(3aR*arU\"[Y[&m,zql}<55n_hU7\c0VP?1!IGdU2O+igaX\w/'JXitmA]6N`",
        r" `?S/D7N<c!*?&$=IY@-{2n\"DphNh;g'\d\"^ )zO/r|cN%6`5",
        r" `f\jG\|7&Gr/mC#CZERlxUu!^;`",
        r" `)<}BT<?oS~F>\")&asY9(-Wsckh%rr}j4?[q&7gh]XCFCKq=@n7y2khE.1/@,1coAzNWgNmMz7[-{\"i`",
        r"`Uu8e<kx/M&kB)0!,XMsb[[kX;2P.:j|+7`z",
        r" `,bQar6DP$hT^'w|^00d1}Z@IWYb6D%?uA?>DR,K&iz@^eh>}Li*:Niz1aOrvGM?h>[?F5r/ti@QxC%IoK|* %\1\y'5gS`",
        r" `^.MFOhA;o1RG,a:5+m?,`",
        r"`.yCTvV<s&*=smX-9*%:Xz`s",
        r" `RJ`",
        r" `]s&&5b^@0|\"E]Pz^z]# @:X];FIXrngifU1]u'K{J/eSpV&F}Jz#}( l*4P:ur^Q}Q2N0eKF$W:;SKld#7sr~lR`",
        r"`)ny6*/yW2$>7YY~{:#Ajrox,p[jwF_wC3<XQLA,)$j<6' KF7!B5.sK#B!Uj,h2UE$kW]HO:L}R/mO`",
        r" `_Zj5\=%MF<&o_\"wgq002f})\,U^O'w8Dx8{IOi].t(2O4WYP:1uKgtgC0 4cky>]~Sf%^`",
        r"`bs?u+)RCNOpgC(UM3&XSMtx8)_j+i>$+e,#sj|x%`",
        r"` 7K*:9t^B]aU,_qVGe5x5h&JO4!m:GW3FDym=qhVr<ZRRM4Pq'VG7\GNT2Jn2.mk#c/PCzBr4m*)\0 Au]TxcW7j\"|`t",
        r" `eOm$mFN1-dMjx\"36G=6{Z/<Tu+CkO`d",
        r" `hbNYJH)=[qM &WCoqm6WNEt1b.O.mwL%TSIppo^<<_gQ3Z;kZ8\0w`D",
        r"`mPgA/(tvL#4;GA.SlVBR3+>tml@@xb*3]/K>2P}iG;s|HR.?/hi#OmaADLW9Wq7K dtIg[gY1K#p)[s8nj~|xU2`u",
        r" `<J+HyZ $X-k6DXc-n\S,8qOw2xDVJ%.Y~iK:MO 3}<Hx2n+aJKlS;A[:;zkaJb0X,Dyc~Y^oOH%R#`",
        r" `lm+P3z&Q7\XC*!9X\@&Pl4ubZ\"~Qk3yINB#~OEvm[ck6P18(9)y!'2,'m)~j/gTP-e)HV7<dl>v//>Cz[U^ bGo:0_^`",
        r"`L_U!Hc1uz|-MstBD$/W&Uq)8qg1q)A(q`",
        r" `*|]%h6O!(g,hNA|>w_kce>d7exP#K4f'%}21;A3q64&UVP,5xAo\"!KrW;Gx3qt77rn|\+ri@S?mNE/du<?4.f|c/%cX+}*A`Z",
        r"`~rLE!9Yxn_THQr>?P/=@6\#yY`P",
        r" `>yf2x-aRXe;GQ{x-!3Yy=6P%9o$7BM=a9v<y7!'N.h?aK;]4 6Ia\Ox, ;z}7$0@-=zd*r,_#CCNd<cBujRVB6oVhCu:cQV}*6=i`Y",
        r"`T94c#wS6S>C-LQO71Qkas#4_l%%5I=:lGC)[R0c^qGc& 6{2X}?y]~IBpbyZY;`Z",
        r" `)6*I?95H!$*l0p~\"3C*&]8O?@;R7Tvb>?4|AaV:A??:Um2{Lv|d5X=jFxr;8 *`-",
        r"`GACiD1xA1r9u*&}HP_f];r5~-]}EXCUhPrpDzy`",
        r" `JPdzQ2QqF_AQl=t]`",
        r" `97P}j:' :MJhH,JnFCVlE\"pX cM/j6!s:=69Wf>Yc[5mb9z)W?Hb5m{Lt,)f,&x<mr'C3NBDMnr6<'|-b6`>",
        r" `@ ~7JyWy/V9V<th:}y.#``S",
        r" `- 3]1f{I**4Q).6}/#BrEPW.2^v]4n6oia8Xu_fOgh:q_E9Qxp}n:p T)*EId99,[7w^&AX(uQ_7~$)DX*z=t].qLh+ON>sMOt}`",
    ),
)
def test_python_rst_backticks_positive(s):
    assert HOOKS['rst-backticks'].search(s)

@pytest.mark.parametrize(
    's',
    (
        " ``[code]``",
        'i like _`kitty`',
        'i like `_`',
        'i like `kitty`_',
    ),
)
def test_python_rst_backticks_negative(s):
    assert not HOOKS['rst-backticks'].search(s)
