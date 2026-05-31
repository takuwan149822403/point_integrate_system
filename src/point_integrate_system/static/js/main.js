(function ($) {
  "use strict";

  function trimTextInputs($form) {
    $form.find('input[type="text"], input[type="email"]').each(function () {
      var $input = $(this);
      $input.val($.trim($input.val()));
    });
  }

  function markEmptyRequiredFields($form) {
    var hasError = false;
    $form.find('[required]').each(function () {
      var $input = $(this);
      if (!$.trim($input.val())) {
        $input.addClass('is-invalid');
        hasError = true;
      } else {
        $input.removeClass('is-invalid');
      }
    });
    return hasError;
  }

  $(function () {
    $('[data-confirm-logout="true"]').on('click', function (event) {
      if (!window.confirm('ログアウトします。よろしいですか？')) {
        event.preventDefault();
      }
    });

    $('.auth-form').on('submit', function (event) {
      var $form = $(this);
      trimTextInputs($form);
      if (markEmptyRequiredFields($form)) {
        event.preventDefault();
        window.alert('必須項目を入力してください。');
        return;
      }
      $form.find('button[type="submit"]').prop('disabled', true).text('送信中...');
    });

    $('#password').on('input', function () {
      var value = $(this).val() || '';
      if (value.length > 0 && value.length < 8) {
        $(this).addClass('is-invalid');
      } else {
        $(this).removeClass('is-invalid');
      }
    });
  });
})(window.jQuery);
