let limitChar = (element) => {
  const maxChar = 250;
  
  let ele = document.getElementById(element.id);
  let charLen = ele.value.length;
  
  let p = document.getElementById('charCounter');
  p.innerHTML = maxChar - charLen + ' characters remaining';
  
  if (charLen > maxChar) 
  {
      ele.value = ele.value.substring(0, maxChar);
      p.innerHTML = 0 + ' characters remaining'; 
  }
}

$(function () {
  
  // Submit Onclick Event
  $('#identify').on('click', function () {
    // get input "headline news"
    let title = $('#headline').val();
    // compute SAN from ajax with title as data
    $.ajax({
      type: 'GET',
      url: "/identify",
      data: {
        'title': title,
      },
      dataType: "json",
      error: function (xhr) {
        alert('something wrong')
      },
      success: function (res) {
        $('#result-section').prop('hidden', false);
        $('#result-judul').html(res.judul)

        $('#prediksi').removeClass('bg-danger');
        $('#prediksi').removeClass('bg-success');
        if (res.is_clickbait) {
          $('#prediksi').addClass('bg-danger');
          $('#prediksi').find('.text').html('CLICKBAIT')
        } else {
          $('#prediksi').addClass('bg-success');
          $('#prediksi').find('.text').html('BUKAN CLICKBAIT')
        }
        $('html, body').animate({
          scrollTop: $("#prediksi").offset().top
        }, 0);
      }
    })
  })
  //End
})