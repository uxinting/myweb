!function($) {
	$(function() {
	
		//Back to top icon functions回到顶端，控制回到顶部图标的显隐
		$(document).scroll(function() {
			if ($(this).scrollTop() > 0) {
				$('.icon-backtop').show();
			} else {
				$('.icon-backtop').hide();
			}
		});
		
		//自动上滚
		$('.icon-backtop').click(function() {
			var id = setInterval(moveTop, 10);
			function moveTop() {
				$(document).scrollTop($(document).scrollTop() / 1.2);
				if ($(document).scrollTop() < 1)
					clearInterval(id);
			}
		});
		
		//prev button上一篇
		$('.icon-prev').click(function() {
			
		});
		
		//next button下一篇
		$('.icon-next').click(function() {
		
		});
		
		//data-toggle
		$('[data-toggle="tooltip"]').mouseover(function() {
			$(this).tooltip('show');
		});
		
		//highlight 文章高亮效果
		$(document).mousemove(function(e) {
			var yy = e.clientY;
			var y = e.pageY;
			if ($('.article').data('highlight') != true) return;
			
			var article = $('.article');
			var ot = article.offset().top;
			if (y > ot && y < ot + article.height()) {
				article.addClass('highlight').css('background-position', '0px ' + yy + 'px');
			} else {
				article.removeClass('highlight');
			}
		});
		
		//当Input失去焦点时检查内容，要有一个hidden的id为hasError的input作为结果保存
		var inputs = $('form').find('input');
		if (typeof(inputs) != 'undefined') {
			for (var i = 0; i < inputs.length; i ++) {
				$(inputs[i]).bind('blur', function(e) {
					var cinput = $(this);
					if (typeof(cinput.data('check')) == 'undefined') return;
					
					var rs = {};
					//email check
					if (cinput.data('check') == 'email') {
						var rs = checkEmail(cinput.val());
						if (rs.status) {//成功之后应发送到服务器检验重复
							cinput.parents('.control-group').removeClass('error').addClass('success');
							
							//ajaxcheck
							ajaxCheckForm({
								data: {input: 'email', value: cinput.val()},
								success: function(data) {
									rs = data;
								}
							});
						}//if
					}//if
					
					//password check
					if (cinput.data('check') == 'password') {
						var rs = checkPasswd(cinput.val());
					}//if
					
					if (cinput.data('check') == 'password-confirm') {
						if ($('#inputPassword').val() != $('#inputPassword2').val()) {
							rs['status'] = false;
							rs['msg'] = '密码不一致'
						} else {
							rs['status'] = true;
							rs['msg'] = '';
						}
					}
					
					//nickname check
					if (cinput.data('check') == 'nickname') {
						var rs = checkNickname(cinput.val());
						if (rs.status) {
							//ajax check
							ajaxCheckForm({
								data: {input: 'nickname', value: cinput.val()},
								success: function (data) {
									rs = data;
								}
							});
						}//if
					}//if
					
					var cg = cinput.parents('.control-group')
					if (rs.status) {
						if (cg.hasClass('error')) {
							cg.removeClass('error');
						}
						cg.addClass('success');
						cinput.next('span').text(rs.msg);
						$('#noError').val('true');
					} else {
						if (cg.hasClass('success')) {
							cg.removeClass('success');
						}
						cg.addClass('error');
						cinput.next('span').text(rs.msg);
						$('#noError').val('false');
					}
				});
			}//for
		}//if
		
		//form submit check
		$('form').submit(function() {
			if($('#noError').val() == false) {
				return false;
			}
		});
		
		//控制某个div消失
		$('.btn').click(function() {
			var dmid = $(this).data('dismiss');
			if (typeof(dmid) != 'undefined') {
				$('#'+dmid).hide();
			}
		});
		
		//ajax safe post
		$.ajaxSetup({
		    crossDomain: false, // obviates need for sameOrigin test
		    beforeSend: function(xhr, settings) {
		        if (!csrfSafeMethod(settings.type)) {
		            xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
		        }
		    }
		});
	});
	
}(window.jQuery);

//检查邮箱
function checkEmail(email) {
	//字母或下划线开头和结尾，由下划线，字母数字组成@前部分，@后由字母或下划线开头和结尾，点号，后加两或三位字母
	var re = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/;
	if (re.test(email)) {
		return {status: true, msg: ''};
	} else {
		return {status: false, msg: '不是一个邮箱'};
	}
}

//检查密码
function checkPasswd(pw) {
	//字母、数字、特殊字符 大于8位
	
	var rs = {};
	//门槛：字母，下划线，数字，特殊字符 8-22位
	var gate = /^[\_\@A-Za-z0-9\!\#\$\%\^\&\*\.\~]{8,22}$/;
	if (!gate.test(pw)) {
		rs['status'] = false;
		rs['msg'] = '8-22位由字母，下划线，数字和特殊字符组成';
		return rs; 
	}
	
	//只有数字或字母
	var only = /(^\d+$)|(^[a-zA-Z]+$)/;
	if (only.test(pw)) {
		rs['status'] = true;
		rs['msg'] = '弱';
		return rs;
	}
	
	//只有数字和字母
	var two = /^[a-zA-Z0-9]{8,22}$/;
	if (two.test(pw)) {
		rs['status'] = true;
		rs['msg'] = '中';
		return rs;
	}
	
	rs['status'] = true;
	rs['msg'] = '强';
	return rs;
}

//检查昵称
function checkNickname(nickname) {
	var re = /^[a-zA-Z0-9\_]{4,16}$/;
	if (!re.test(nickname)) {
		return {status: false, msg: '4-16位由数字、字母、下划线组成'}
	}
	
	return {status: true, msg: ''}
}

//csrf django functions
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

//ajax检验
//opt.data opt.success=callback
function ajaxCheckForm(opt) {
	$.ajax({
		type: 'POST',
		async: false,
		url: location.pathname,
		dataType: 'json',
		data: opt.data,
		success: opt.success,
		error: function(e, msg) {
			alert(msg)
		}
	});
}

//激活
function activate() {
	var email = $('[type="email"]').val();
	$.get('/accounts/activate?email='+email, function(data, status) {
			if (status == 'success') {
				$('#error').text(data).next('span').remove();
			} else {
				$('#error').text('网络错误，请稍后再试').next().remove();
			}
		}
	);
}

//换验证码
function changeVerify() {
	$('#inputVerify').next('img').attr('src', '/accounts/verify?time=' + new Date().getTime());
}
