$(function () {

  // Submit Onclick Event
  $('#identify').on('click', function () {
    // get input "headline news"
    let title = $('#headline').val();
    let model = $('input[name="model"]:checked').val()

    // compute SAN from ajax with title as data

    $.ajax({
      type: 'GET',
      url: "/identify",
      data: {
        'title': title,
        'model': model
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