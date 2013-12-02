chrome.extension.sendMessage({}, function(response) {
	var readyStateCheckInterval = setInterval(function() {
	if (document.readyState === "complete") {
		clearInterval(readyStateCheckInterval);

		rangy.init();
		var highlighter = rangy.createHighlighter();

                highlighter.addClassApplier(rangy.createCssClassApplier("highlight", {
		        ignoreWhiteSpace: true,
		        tagNames: ["span", "a"]
		    }));

		var range = rangy.createRange();
		range.selectNodeContents(document.body);

		var aSendButtonTemplate = $('<div>',{ role:'button' ,text: 'One-Timer', 'data-tooltip': 'send a self-destructing mail', class:'one-time-button T-I J-J5-Ji aoO T-I-atl L3 One_Time_Button_Identifier' ,'data-tooltip-delay':'800'} );
		aSendButtonTemplate.html('<img role="button" style="padding-top:0px;" ' + 'src="' +         chrome.extension.getURL('icons/explodingMail28.png') + '" alt="">'  );

	  	insert_items_everytime(get_send_button,aSendButtonTemplate,'One_Time_Button_Identifier','after',replace_content_with_image);


	}
	}, 10);
});

	 insert_items_everytime = function(get_items_function,jqueryObject,unique_identifier, beforeOrAfter, functionOnClick) {
		$('body div.nH').contents().on('mouseover','.nH[role="main"]',function(){
			var items = get_items_function();
			$(items).each(function(loopindex,loopitem){
				if( !$(this).hasClass(unique_identifier) ) {
					var id = Math.floor(Math.random($(this).parent().parent().length)*16777215).toString(16);
					var newJqueryObject = $(jqueryObject).clone();
					newJqueryObject.attr("id",id);
					if (beforeOrAfter == 'before')
						$(items[loopindex]).before(newJqueryObject);
					else {
						$(items[loopindex]).after(newJqueryObject);
					     }
					newJqueryObject.mousedown(functionOnClick);

					$(this).addClass(unique_identifier);	// so it will add this only once.
				}

			});
			return;
		});
	  };

	 replace_content_with_image = function() {

		var highlighter = rangy.createHighlighter();

                highlighter.addClassApplier(rangy.createCssClassApplier("highlight_selected_to_remove", {
		        ignoreWhiteSpace: true,
		        tagNames: ["span", "a"]
		    }));
      		highlighter.highlightSelection("highlight_selected_to_remove");
		var sel = rangy.getSelection();
		var selectionHtml = sel.toHtml();
		var numberOfRanges = sel.rangeCount;

		
		var activating_button = this;
		var content_item = find_the_closest_compose(this);
		var text = content_item.text();
		var contentHtml = content_item.html();

		var contentToReplace;
		if (numberOfRanges > 0) {
			contentToReplace = selectionHtml; 
		}
		else {
			contentToReplace = contentHtml;
		}
		if (contentToReplace == '') { contentToReplace = contentHtml; }
		var contentHtmlCorrected = replace_unused_text(contentToReplace);


		var get_url = 'http://expired-mail.liorkirsch.webfactional.com/addViewlimited?text=' +  encodeURIComponent(text) + '&html=' + encodeURIComponent(contentHtmlCorrected);;
		var posturl = 'http://expired-mail.liorkirsch.webfactional.com/addViewlimited';

	//	var get_url = 'http://localhost:8000/addViewlimited?text=' +  encodeURIComponent(text) + '&html=' + encodeURIComponent(contentHtmlCorrected);			
	//	var post_url = 'http://localhost:8000/addViewlimited';
		get_url = get_url.trim();

		/*$.ajax({
			type: "POST",
			//the url where you want to sent the userName and password to
			url: post_url,
			dataType: 'json',
			data: JSON.stringify({ "text": text ,"html": contentHtmlCorrected}),
			success: function (json) {
				var imageString = '<div><img src="' + json.image_url + '" alt="Inline image 1"> </div>';
		  	        content_item.html(imageString);
			}
		    });*/

	/*	$.post(post_url, JSON.stringify({ "text": text ,"html",contentHtmlCorrected}) )
		  .done(function( json ) {
			var imageString = '<div><img src="' + json.image_url + '" alt="Inline image 1"> </div>';
	  	        content_item.html(imageString);
		  });
	*/
		$.getJSON( get_url, function( json ) {
			var imageString = '<img src="' + json.image_url + '" alt="Inline image 1"> ';
			var currentContent = content_item.html();
			var elementsToRemove = $('.highlight_selected_to_remove');
			if (elementsToRemove.length > 0) {
				$(elementsToRemove[0]).replaceWith(imageString);
				for (var i=1;i<elementsToRemove.length;i++) {
					$(elementsToRemove[i]).remove();
				}
			}	
			else {	
				content_item.html(imageString);	
			}
//			var newContent = currentContent.replace(new RegExp(contentToReplace, 'g'), imageString);
//	  	        content_item.html(newContent);
		 });
	 }

	 replace_unused_text = function(contentToReplace) {
		var contentHtmlCorrected = contentToReplace.replace(new RegExp('\^<div>', 'g'), '');
		contentHtmlCorrected = contentHtmlCorrected.replace(new RegExp('<div>', 'g'), '\n');
		contentHtmlCorrected = contentHtmlCorrected.replace(new RegExp('</div>', 'g'), '');
		contentHtmlCorrected = contentHtmlCorrected.replace(new RegExp('<span class="highlight_selected_to_remove">', 'g'), '');
		contentHtmlCorrected = contentHtmlCorrected.replace(new RegExp('</span>', 'g'), '');
		contentHtmlCorrected = contentHtmlCorrected.replace(new RegExp('<br>', 'g'), '\n');
		contentHtmlCorrected = contentHtmlCorrected.replace(new RegExp('&nbsp;', 'g'), ' ');
		return contentHtmlCorrected;
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

	 get_send_button = function() {
		return $('body div.nH').find('td.gU.Up div.T-I-atl');
	  };
