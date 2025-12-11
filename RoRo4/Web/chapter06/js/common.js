$(document).ready(function(){
	
	///导航下拉
	$('.g_nav01 table tr td').mouseover(function(){
	
	$(this).find('.nav_tan').stop(true,true).slideDown();
	$(this).children("a").addClass("cur");
	});
	$('.g_nav01 table tr td').mouseleave(function(){
	
	$(this).find('.nav_tan').stop(true,true).slideUp('fast');
	$(this).children("a").removeClass("cur");
	});
	//搜索
	$(".isearch span").click(
	function(){
		$(".search01").toggle();
		}
	)
	
});
function runImg(runBlock, ctrls, pages, auto){
    var page = 0;
    var max_page = Math.ceil(runBlock.find('ul').find('li').length);
    var img_width = runBlock.width();
    runBlock.find('ul').find('li').css('width', img_width);
    runBlock.find('ul').css('width', max_page*img_width);
    if(ctrls){
    	var ctrl_width = 0;
	    for(var i=0; i<max_page; i++){
	        runBlock.find('.ctrl').append('<div></div>');
	        ctrl_width += 20;
	    }
	    runBlock.find('.ctrl').css('margin-left', -ctrl_width/2);
	    runBlock.find('.ctrl div').first().addClass('now');
	    runBlock.find('.ctrl div').click(function(){
	        page = $(this).index();
	        // runBlock.find('ul').animate({'marginLeft':-page*img_width}, 500);
	        runBlock.find('li').hide().css({'opacity':0});
	        runBlock.find('li').eq(page).show().animate({'opacity':1}, 400);
	        runBlock.find('.ctrl div').removeClass('now');
	        $(this).addClass('now');
	    });
    }
    if(pages){
    	runBlock.find('.next').click(function(){
	        page++;
	        if(page >= max_page){
	            page = 0;
	        }
	        // runBlock.find('ul').animate({'marginLeft':-page*img_width}, 500);
	        runBlock.find('li').hide().css({'opacity':0});
	        runBlock.find('li').eq(page).show().animate({'opacity':1}, 400);
	        if(ctrls){
	        	runBlock.find('.ctrl div').removeClass('now').eq(page).addClass('now');
	        }
	    });
	    runBlock.find('.prev').click(function(){
	        page--;
	        if(page < 0){
	            page = max_page - 1;
	        }
	        // runBlock.find('ul').animate({'marginLeft':-page*img_width}, 500);
	        runBlock.find('li').hide().css({'opacity':0});
	        runBlock.find('li').eq(page).show().animate({'opacity':1}, 400);
	        if(ctrls){
	        	runBlock.find('.ctrl div').removeClass('now').eq(page).addClass('now');
	        }
	    });
    }
    if(auto){
    	setInterval(function(){
	        page++;
	        if(page >= max_page){
	            page = 0;
	        }
	        // runBlock.find('ul').animate({'marginLeft':-page*img_width}, 500);
	        runBlock.find('li').hide().css({'opacity':0});
	        runBlock.find('li').eq(page).show().animate({'opacity':1}, 400);
	        if(ctrls){
	        	runBlock.find('.ctrl div').removeClass('now').eq(page).addClass('now');
	        }
	    }, 10000);
    }
    // 初始化
    runBlock.find('li').first().show().css({'opacity':1});
}

