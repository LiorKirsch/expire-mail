chrome.extension.sendMessage({}, function(response) {
	var readyStateCheckInterval = setInterval(function() {
	if (document.readyState === "complete") {
		clearInterval(readyStateCheckInterval);



		var jq = document.createElement('script');
		jq.src = "https://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js";
		document.getElementsByTagName('body')[0].appendChild(jq);

		//var anImage = '<img role="button" style="padding-top:4px;" src="' +          chrome.extension.getURL('images/sprite_black2.png') + '" alt="">';
		//aSendButton = $('<div>',{ role:'button' , 'data-tooltip': 'another send', class:'T-I J-J5-Ji aoO T-I-atl L3 anotherSendIdentifier' ,'data-tooltip-delay':'800'} );
		//aSendButton.html(anImage);
		aSendButton = $('<div>',{ role:'button' ,text:'One Timer', 'data-tooltip': 'another send', class:'T-I J-J5-Ji aoO T-I-atl L3 anotherSendIdentifier' ,'data-tooltip-delay':'800'} );
	  	insert_items_everytime(get_send_button,aSendButton,'anotherSendIdentifier','after',replace_content_with_image);


		

	}
	}, 10);
});

		check_item_exists = function(unique_identifier, jqueryItem,beforeOrAfter) {
			var nextItem;			
			if (beforeOrAfter == 'before')
				nextItem = jqueryItem.prev();
			else {
				nextItem = jqueryItem.next();
			     }

			var itemExists = false;

			if (jqueryItem.hasClass('customdec') & jqueryItem.hasClass(unique_identifier) ){
				itemExists = true;
			}
			else {
				if(nextItem.hasClass('customdec') | nextItem.hasClass('customdec')) {
					if(nextItem.hasClass(unique_identifier)) {
						itemExists = true;
					}
					else {	
					itemExists = check_item_exists(unique_identifier, nextItem,beforeOrAfter);
					}
				}
			}
			return itemExists;
		}


		 insert_items_everytime = function(get_items_function,jqueryObject,unique_identifier, beforeOrAfter, functionOnClick) {
			$('body div.nH').contents().on('mouseover','.nH[role="main"]',function(){
				var items = get_items_function();
				$(items).each(function(loopindex,loopitem){
					if(! check_item_exists(unique_identifier, $(this) ,beforeOrAfter) ){
						var id = Math.floor(Math.random($(this).parent().parent().length)*16777215).toString(16);
						var newJqueryObject = $(jqueryObject).clone();
						newJqueryObject.attr("id",id);
						$(newJqueryObject).addClass('customdec');

						if (beforeOrAfter == 'before')
							$(items[loopindex]).before(newJqueryObject);
						else {
							$(items[loopindex]).after(newJqueryObject);
						     }
						
					}
				$('.' + unique_identifier).click(functionOnClick);
				});
				return;
			});
		  };

		 replace_content_with_image = function() {
			var content_item = find_the_closest_compose(this);
			var text = content_item.text();
			var url = 'http://expired-mail.liorkirsch.webfactional.com/addViewlimited?text=' +  encodeURIComponent(text);
//			var url = 'http://localhost:8000/addViewlimited?text=' +  encodeURIComponent(text);
			$.getJSON( url, function( json ) {
				var imageString = '<div><img src="' + json.image_url + '" alt="Inline image 1"> </div>';
		  	        content_item.html(imageString);
			 });
		 }

		 dummy_function = function () {
		 }
		 find_the_closest_compose = function(item) {
			var table = $(item).closest('table.iN');
			return $(table).find('div.editable');
		  }

		 get_reply_button = function() {
			return $('body div.nH').find('tr.acZ td.gH.acX div.T-I-Js-IF');
		  };

		 get_bar = function() {
			return $('body div.nH').find('td.gU.OoRYyc div.aWQ');
		  };

		 get_trashcan_button = function() {
			return $('body div.nH').find('td.gU.az5 div.J-J5-Ji');
		  };

		 get_send_button_cell = function() {
			return $('body div.nH').find('td.gU.Up');
		  };
		 get_send_button = function() {
			return $('body div.nH').find('td.gU.Up div.T-I-atl');
		  };
