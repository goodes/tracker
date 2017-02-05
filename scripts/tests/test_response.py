import pytest
import mock

from update import process_response
TEST_DATA = [
    (
        {
           "banner": "",
           "data_type": "RASHUM",
           "hasSignimage": "",
           "hasimage": "",
           "itemcodeinfo": "There is no information regarding the Registered from Abroad postal item RS3412645"
                           "21CN.<br><br><script async src=\"//pagead2.googlesyndication.com/pagead/js/adsbygo"
                           "ogle.js\"></script><!-- Itemtrace Result desk --><ins class=\"adsbygoogle\" style="
                           "\"display:inline-block;width:531px;height:60px\" data-ad-client=\"ca-pub-413431166"
                           "0880303\" data-ad-slot=\"5138427073\"></ins><script>try{(adsbygoogle = window.adsb"
                           "ygoogle || []).push({})}catch(err){}</script>",
           "sHeader1": "",
           "sHeader2": "",
           "typename": "Registered mail"
        },
        ('GOOD', 'There is no information regarding the Registered from Abroad postal item RS341264521CN.')
    ), (
        {
           "banner": "",
           "data_type": "RASHUM",
           "hasSignimage": "",
           "hasimage": "",
           "itemcodeinfo": "<table width=\"100%\" style=\"border-bottom: 2px ridge rgb(101, 136, 149)\" ><col />"
                           "<col /><col /><col /><tr><td class=\"titlerow\">Date</td><td class=\"titlerow\">Post"
                           "al Unit</td><td class=\"titlerow\">City</td><td class=\"titlerow\">Description</td><"
                           "/tr><tr style=\"border-top: 2px ridge rgb(101, 136, 149)\"><td class=\"datarowB\" st"
                           "yle=\"border-right: 2px ridge rgb(101, 136, 149)\">05/02/2017</td><td class=\"dataro"
                           "wB\" style=\"border-right: 2px ridge rgb(101, 136, 149)\"> Givat Sharet</td><td clas"
                           "s=\"datarowB\" style=\"border-right: 2px ridge rgb(101, 136, 149)\">Beit Shemesh</td"
                           "><td class=\"datarowB\" style=\"border-right: 2px ridge rgb(101, 136, 149)\">Arrived"
                           " at the postal unit for delivery to addressee (shelf no \u05d2-122)</td></tr><tr sty"
                           "le=\"border-top: 2px ridge rgb(101, 136, 149)\"><td class=\"datarow\" style=\"border"
                           "-right: 2px ridge rgb(101, 136, 149)\">02/02/2017</td><td class=\"datarow\" style=\""
                           "border-right: 2px ridge rgb(101, 136, 149)\"> Beit Shemesh</td><td class=\"datarow\""
                           " style=\"border-right: 2px ridge rgb(101, 136, 149)\">Beit Shemesh</td><td class=\"d"
                           "atarow\" style=\"border-right: 2px ridge rgb(101, 136, 149)\">Due to its size or wei"
                           "ght an SMS was sent to the addresse and the item will be forwarded to the postal uni"
                           "t for delivery</td></tr></table><br><br><script async src=\"//pagead2.googlesyndicat"
                           "ion.com/pagead/js/adsbygoogle.js\"></script><!-- Itemtrace Result desk --><ins class"
                           "=\"adsbygoogle\" style=\"display:inline-block;width:531px;height:60px\" data-ad-clie"
                           "nt=\"ca-pub-4134311660880303\" data-ad-slot=\"5138427073\"></ins><script>try{(adsbyg"
                           "oogle = window.adsbygoogle || []).push({})}catch(err){}</script>",
           "sHeader1": "",
           "sHeader2": "",
           "typename": "Registered mail"
        },
        ('GOOD', u'Arrived at the postal unit for delivery to addressee (shelf no \\u05d2-122)'),
    ), (
        {
           "banner": "",
           "data_type": "ERROR01",
           "hasSignimage": "",
           "hasimage": "",
           "itemcodeinfo": "The item code typed is invalid or misstyped, it cannot be recognized by the system."
                           "<br><br><script async src=\"//pagead2.googlesyndication.com/pagead/js/adsbygoogle.j"
                           "s\"></script><!-- Itemtrace Result desk --><ins class=\"adsbygoogle\" style=\"displ"
                           "ay:inline-block;width:531px;height:60px\" data-ad-client=\"ca-pub-4134311660880303"
                           "\" data-ad-slot=\"5138427073\"></ins><script>try{(adsbygoogle = window.adsbygoogle "
                           "|| []).push({})}catch(err){}</script>",
           "sHeader1": "",
           "sHeader2": "",
           "typename": ""
        },
        ('ERROR', 'The item code typed is invalid or misstyped, it cannot be recognized by the system.')
    ), (
        {
           "banner": "",
           "data_type": "RASHUM",
           "hasSignimage": "",
           "hasimage": "",
           "itemcodeinfo": "There is no information regarding the Registered from Abroad postal item RE4695539"
                           "71SE.<br><br><script async src=\"//pagead2.googlesyndication.com/pagead/js/adsbygo"
                           "ogle.js\"></script><!-- Itemtrace Result desk --><ins class=\"adsbygoogle\" style="
                           "\"display:inline-block;width:531px;height:60px\" data-ad-client=\"ca-pub-413431166"
                           "0880303\" data-ad-slot=\"5138427073\"></ins><script>try{(adsbygoogle = window.adsby"
                           "google || []).push({})}catch(err){}</script>",
           "sHeader1": "",
           "sHeader2": "",
           "typename": "Registered mail"
        },
        ('GOOD', 'There is no information regarding the Registered from Abroad postal item RE469553971SE.')
    ), (
        {
           "banner": "",
           "data_type": "ERROR06",
           "hasSignimage": "",
           "hasimage": "",
           "itemcodeinfo": "\u05d1\u05e8\u05e7\u05d5\u05d3 8000502460212 \u05dc\u05d0 \u05d7\u05d5\u05e7\u05d9<br"
                           "><br><script async src=\"//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js\"></"
                            "script><!-- Itemtrace Result desk --><ins class=\"adsbygoogle\" style=\"display:inlin"
                            "e-block;width:531px;height:60px\" data-ad-client=\"ca-pub-4134311660880303\" data-ad-"
                            "slot=\"5138427073\"></ins><script>try{(adsbygoogle = window.adsbygoogle || []).push({"
                            "})}catch(err){}</script>",
           "sHeader1": "",
           "sHeader2": "",
           "typename": ""
        },
        ('ERROR', '\\u05d1\\u05e8\\u05e7\\u05d5\\u05d3 8000502460212 \\u05dc\\u05d0 \\u05d7\\u05d5\\u05e7\\u05d9')
    ), (
        {
           "banner": "",
           "data_type": "ERROR01",
           "hasSignimage": "",
           "hasimage": "",
           "itemcodeinfo": "The item code typed is invalid or misstyped, it cannot be recognized by the system.<br>"
                           "<br><script async src=\"//pagead2.googlesyndication.com/pagead/js/adsbygoogle.js\"></sc"
                           "ript><!-- Itemtrace Result desk --><ins class=\"adsbygoogle\" style=\"display:inline-bl"
                           "ock;width:531px;height:60px\" data-ad-client=\"ca-pub-4134311660880303\" data-ad-slot="
                           "\"5138427073\"></ins><script>try{(adsbygoogle = window.adsbygoogle || []).push({})}catc"
                           "h(err){}</script>",
           "sHeader1": "",
           "sHeader2": "",
           "typename": ""
        },
        ('ERROR', 'The item code typed is invalid or misstyped, it cannot be recognized by the system.')
    )
]

def test_all():
    for d, expected in TEST_DATA:
        assert expected == process_response(d)
