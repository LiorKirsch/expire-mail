$(document).ready(function(){



 	var loadButtons = function(items){
            $(items).each(function(loopindex,loopitem){
                if(!$(this).prev().hasClass('customdec')){
                    var id = Math.floor(Math.random($(this).parent().parent().length)*16777215).toString(16);
                    var decryptButton = [ '<a decid="',
                                          id,
                                          '" customFunction="decrypt" ',
                                          'class="T-I J-J5-Ji T-I-Js-IF aaq T-I-ax7 L3 customdec" ',
                                          'style="position:relative;top:7px" role="button" ',
                                          'tabindex="0" style="-webkit-user-select: none; " ',
                                          'aria-label="Decrypt Message" data-tooltip="Decrypt Message">',
                                          '<img role="button" style="padding-top:4px;" ', 
                                          'src="',
                                          chrome.extension.getURL('images/sprite_black2.png'),
                                          '" alt="">',
                                          '</a>' ].join('')
                    var verifyButton = [ '<a id="'+id+'" customFunction="verify" ',
                                          'class="T-I J-J5-Ji T-I-Js-IF aaq T-I-ax7 L3 customdec" ',
                                          'style="position:relative;top:7px" role="button" ',
                                          'tabindex="0" style="-webkit-user-select: none; " ',
                                          'aria-label="Verify Message" data-tooltip="Verify Message">',
                                          '<img role="button" style="padding-top:4px;" ', 
                                          'src="',
                                          chrome.extension.getURL('images/verify.png'),
                                          '" alt="">',
                                          '</a>' ].join('')

                    $(items[loopindex]).before(decryptButton + verifyButton);
                };
            });
        };

	//Old theme support for the compose email section
        var loadComposeButtons = function(searchLocation){
            $('span.es.el:contains(»)',searchLocation).each(function(){
                if(!$(this).prev().hasClass('customdec')){
                    var id = Math.floor(Math.random($(this).parent().parent().length)*16777215).toString(16);
                    var newButton = $(this).before(
                        ['<span class="es el customdec" ><a id="'+id+'" customFunction="encrypt">Encrypt Message</a></span><span style="position:relative;top:-5px;">&nbsp;&nbsp;</span>',
                         '<span class="es el customdec" ><a id="'+id+'" customFunction="composer">Compose Message In Popup</a></span><span style="position:relative;top:-5px;">&nbsp;&nbsp;</span>',
                         '<span class="es el customdec" ><a id="'+id+'" customFunction="sign">Sign Message</a> </span><span class="customdec" style="position:relative;top:-5px;">&nbsp;&nbsp;</span>'].join(''));
                };
            });
        };

	//Load up buttons on keypress
        //Load up buttons on mouseover
        //Tiny timeout is required so that the html can be rendered
        setTimeout(function(){
            $('body div.nH').contents().on('mouseover','.nH[role="main"]',function(){
                //loadOldThemesButtons(this);
                loadComposeButtons(this);
                loadButtons($(this).find('tr.acZ td.gH.acX div.T-I-Js-IF')); 
                loadGenericFunctionHandlers(this);
            });

            /*$('body div.nH').contents().keypress(function(e){
                loadButtons($('body div.nH').contents().find('tr.acZ td.gH.acX div.T-I-Js-IF')); 
                var highLevelCheck = $('body div.nH').contents().find('.nH');
                loadGenericFunctionHandlers(highLevelCheck);
                //loadOldThemesButtons(highLevelCheck);
                loadComposeButtons(highLevelCheck);
            });
            */
        },1000);


});
