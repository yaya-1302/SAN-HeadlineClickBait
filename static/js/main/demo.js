let limitChar = (element) => {
  const maxChar = 250;
  
  let ele = document.getElementById(element.id);
  let charLen = ele.value.length;
  
  let p = document.getElementById('charCounter');
  p.innerHTML = maxChar - charLen + ' characters remaining';
  
  if (charLen > maxChar) 
  {
      p.innerHTML = 'Limit exceeded'; 
  }
}

$.fn.maxCharWarning = function() {

  return this.each(function() {
    var el                    = $(this),
        maxLength             = el.data('max-length'),
        warningContainerClass = el.data('max-length-warning-container'),
        warningContainer      = $('.'+warningContainerClass)
    ;
    el.keyup(function() {
      var length = el.val().length;      
      if (length >= maxLength){
        el.addClass('input-error');
      }
      else if (length < maxLength) {
        el.removeClass('input-error');
      }
    });
  });
};

$('.js-max-char-warning').maxCharWarning();

$(function () {
  
  // Submit Onclick Event
  $('#identify').on('click', function () {
    // get input "headline news"
    let title = $('#headline').val();
    // compute SAN from ajax with title as data
    const btn = document.querySelector(".btn-custom");
    btn.classList.toggle("btn-loading")

    $.ajax({
      type: 'GET',
      url: "/identify",
      data: {
        'title': title,
      },
      dataType: "json",
      error: function (xhr) {
        $('#identify').removeClass('btn-loading');
        alert('Judul tidak dapat diidentifikasi');
      },
      success: function (res) {
        $('#identify').removeClass('btn-loading');

        $('#result-section').prop('hidden', false);
        $('#result-judul').html(res.judul)

        $('#prediksi').removeClass('bg-danger');
        $('#prediksi').removeClass('bg-success');
        if (res.is_clickbait) {
          $('#prediksi').addClass('bg-danger');
          $('#prediksi').find('.text').html('CLICKBAIT')
          $('#prediksi').find('.accuracy').html(res.accuracy)
        } else {
          $('#prediksi').addClass('bg-success');
          $('#prediksi').find('.text').html('BUKAN CLICKBAIT')
          $('#prediksi').find('.accuracy').html(res.accuracy)
        }
        $('html, body').animate({
          scrollTop: $("#prediksi").offset().top
        }, 0);

      }
    })
  })
  //End
})