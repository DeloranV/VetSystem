$('#remove_user').on('click', function(){
      var $user_id = $('#remove_id').val();

      $.ajax({
        url: '/api/users/'.concat($user_id, '?key=1111'),
        method: 'DELETE'
      }).done(function(data){
        $.ajax({
          url: '/users',
          method: 'GET'
        }).done(function(data){
          $('body').html(data);
        });
      });
    });
$('.user_id').on('click', function(){
    if($('#option_select').length == 0){

      var $clicked_id = $(this).text();

      var $option_select = $("<select>")
      .attr('id', 'option_select');

      var $name_option = $("<option value='name'>Imie</option>");
      var $surname_option = $("<option value='surname'>Nazwisko</option>");
      var $email_option = $("<option value='email'>Adres e-mail</option>");
      var $phone_option = $("<option value='phone'>Numer telefonu</option>");

      var $change_line = $('<input>')
      .attr('type', 'text')
      .attr('id', 'change_line');

      var $change_submit = $("<input>")
      .attr('type', 'button')
      .attr('id', 'change_submit')
      .attr('value', 'Zmień');

      $('#modify_container').append($option_select);
      $('#option_select').append($name_option);
      $('#option_select').append($surname_option);
      $('#option_select').append($email_option)

      $('#modify_container').append($change_line);

      $('#modify_container').append($change_submit);

      $('#change_submit').on('click', function(){
        var $changed_attr = $('#option_select').val();
        var $changed_val = $('#change_line').val();

        var data_object = {};
        data_object[$changed_attr] = $changed_val;

        $.ajax({
          url: '/api/users/'.concat($clicked_id, '?key=1111'),
          method: 'PATCH',
          data: JSON.stringify(data_object),
          contentType: 'application/json'
        }).done(function(data){
          $.ajax({
          url: '/users',
          method: 'GET'
          }).done(function(data){
            $('body').html(data);
          });
        });

        $('#change_submit').remove();
        $('select').remove();
        $('#change_line').remove();
  });
};
});