$(function(){
    $("#pageIndex .contactsBox a").click(function () {
    	$(".cover").show();
    })
    // cover获取标签
    // 关闭cover
    $(".cover .closeBtn").click(function () {
    	$(".cover").hide();
    })
	// 滑动块start
    var tag1 = false, ox1 = 0, left1 = 0, bgleft1 = 0;
    var tag2 = false, ox2 = 0, left2 = 0, bgleft2 = 0;
    $('.progress_Right').mousedown(function(e) {
      ox1 = e.pageX - left1;
      tag1 = true;
    });
    $('.progress_Left').mousedown(function(e) {
      ox2 = e.pageX - left2;
      tag2 = true;
    });
    $(document).mouseup(function() { tag1 = tag2 = false; });
    $('.progress').mousemove(function(e) {//鼠标移动
      if (tag1) {
        left1 = e.pageX - ox1;
        if (left1 <= left2) {
          left1 = left2;
        }else if (left1 > 400) {
          left1 = 400;
        }
        $('.progress_Right').css('left', left1);
        $('.progress_bar').width(left1 - left2);
        $('.textRight').html(parseInt((left1/400)*100));
      }
      if (tag2) {
        left2 = e.pageX - ox2;
        if (left2 <= 0) {
          left2 = 0;
        }else if (left2 > left1) {
          left2 = left1;
        }
        $('.progress_Left').css('left', left2);
        $('.progress_bar').width(left1 - left2).css('left', left2);
        $('.textLeft').html(parseInt((left2/400)*100));
      }
    });
    // 滑动块end
    // cover滑动块
    var tag3 = false, ox3 = 0, left3 = 0, bgleft3 = 0;
    $('.coverProgress').mousedown(function(e) {
      ox3 = e.pageX - left3;
      tag3 = true;
    });
    $(document).mouseup(function() { tag3 = false; });
    $('.coverProgress').mousemove(function(e) {//鼠标移动
      if (tag3) {
        left3 = e.pageX - ox3;
        if (left3 <= 0) {
          left3 = 0;
        }else if (left3 > 150) {
          left3 = 150;
        }
        $('.coverProgress_btn').css('left', left3);
        $('.coverProgress_bar').width(left3);
        $('.coverText').html(parseInt((left3/150)*100));
      }
    });
    $('.coverProgress_bg').click(function(e) {//鼠标点击
     if (!tag3) {
      bgleft3 = $('.coverProgress_bg').offset().left;
      left3 = e.pageX - bgleft3;
      if (left3 <= 0) {
       left3 = 0;
      }else if (left3 > 150) {
       left3 = 150;
      }
      $('.coverProgress_btn').css('left', left3);
      $('.coverProgress_bar').animate({width:left3},300);
      $('.coverText').html(parseInt((left3/150)*100));
     }
    });
});