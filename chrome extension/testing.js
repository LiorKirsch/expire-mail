var jq = document.createElement('script');
jq.src = "https://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js";
document.getElementsByTagName('body')[0].appendChild(jq);


check_item_exists = function(unique_identifier, jqueryItem) {
	var previousItem = jqueryItem.prev();
	var itemExists = false;
	if(previousItem.hasClass('customdec')) {
		if(previousItem.hasClass(unique_identifier)) {
			itemExists = true;
		}
		else {	
		itemExists = check_item_exists(unique_identifier, previousItem);
		}
	}
	return itemExists;
}


 insert_before_reply_button_everytime = function(jqueryObject,unique_identifier) {
	$('body div.nH').contents().on('mouseover','.nH[role="main"]',function(){
		var reply_buttons = get_reply_button();
		$(reply_buttons).each(function(loopindex,loopitem){
			if(! check_item_exists(unique_identifier, $(this) ) ){
				$(jqueryObject).addClass('customdec');
				$(reply_buttons[loopindex]).before(jqueryObject);
			}

		});
		return;
	});
  };

 get_reply_button = function() {
	return $('body div.nH').find('tr.acZ td.gH.acX div.T-I-Js-IF');
  };

aNewLink = $('<a>',{ text: 'new button', title: 'Blah', href: 'http://www.google.com', class:'T-I J-J5-Ji T-I-Js-IF aaq T-I-ax7 L3 myIdentifier' } );
 insert_before_reply_button_everytime(aNewLink,'myIdentifier');

