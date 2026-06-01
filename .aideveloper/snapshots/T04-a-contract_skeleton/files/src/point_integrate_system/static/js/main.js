/* global $ */
$(function () {
  $('.js-toggle-password').on('click', function () {
    var target = $(this).data('target');
    var $input = $(target);
    if (!$input.length) {
      return;
    }
    var nextType = $input.attr('type') === 'password' ? 'text' : 'password';
    $input.attr('type', nextType);
    $(this).text(nextType === 'password' ? '表示' : '非表示');
  });

  $('.js-confirm').on('click', function (event) {
    var message = $(this).data('confirm-message') || '処理を続行しますか？';
    if (!window.confirm(message)) {
      event.preventDefault();
    }
  });

  $('.js-auth-form').on('submit', function (event) {
    var $form = $(this);
    var missing = [];
    $form.find('[required]').each(function () {
      if (!String($(this).val() || '').trim()) {
        missing.push($(this).attr('name') || $(this).attr('id'));
      }
    });
    if (missing.length > 0) {
      event.preventDefault();
      window.alert('必須項目を入力してください: ' + missing.join(', '));
    }
  });
});
