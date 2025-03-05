  $('#remove_app').on('click', function(){
    var $app_id = $('#remove_id').val();

    $.ajax({
      url: '/api/appointments/'.concat($app_id, '?key=1111'),
      method: 'DELETE'
    }).done(function(data){
      $.ajax({
        url: '/appointments',
        method: 'GET'
      }).done(function(data){
        $('body').html(data);
      });
    });
  });

    $('.app_id').on('click', function(event){ //ZMIENIC NA KLIKANIE NA ID I POTEM WYBRAC CO SIE CHCE ZMIENIC I PRZESYLANIE ID W AJAX
    if($('#modify_select').length == 0){

      var $clicked_id = $(this).text();

      var $option_select = $("<select>")
      .attr('id', 'modify_select');

      var $scheduled_option = $("<option value='scheduled'>Termin wizyty</option>");

      var $change_line = $('<input>')
      .attr('type', 'text')
      .attr('id', 'change_line')
      .attr('placeholder', 'RRRR-MM-DD HH:MM:SS')

      var $change_submit = $("<input>")
      .attr('type', 'button')
      .attr('id', 'change_submit')
      .attr('value', 'Zmień');

      $('#modify_container').append($option_select);
      $('#modify_select').append($scheduled_option);

      $('#modify_container').append($change_line);

      $('#modify_container').append($change_submit);

      $('#change_submit').on('click', function(){
        var $changed_attr = $('#modify_select').val();
        var $changed_val = $('#change_line').val();

        var data_object = {}
        data_object[$changed_attr] = $changed_val

        $.ajax({
          url: '/api/appointments/'.concat($clicked_id, '?key=1111'),
          method: 'PATCH',
          data: JSON.stringify(data_object),
          contentType: 'application/json'
        }).done(function(data){
          $.ajax({
          url: '/appointments',
          method: 'GET'
          }).done(function(data){
            $('body').html(data);
          });
        });

        $('#change_submit').remove();
        $('#modify_select').remove();
        $('#change_line').remove();
      });
    };
 });