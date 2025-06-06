dc$('#add_pet').on('click', function(){
        if($('#name_input').length == 0) {

          var $name_label = $('<label>Imie zwierzęcia</label>');
          var $name_input = $('<input>')
          .attr('id', 'name_input')
          .attr('type', 'text');

          var $type_label = $('<label>Rodzaj zwierzęcia</label>');
          var $type_input = $('<input>')
          .attr('id', 'type_input')
          .attr('type', 'text');

          var $age_label = $('<label>Wiek zwierzęcia</label>');
          var $age_input = $('<input>')
          .attr('id', 'age_input')
          .attr('type', 'text');

          var $submit_button = $('<input>')
          .attr('type', 'button')
          .attr('id', 'submit_button')
          .attr('value', 'Zarejestruj');

          $('#add_pet_box').append($name_label, $name_input, $type_label, $type_input, $age_label,
                          $age_input, $submit_button);

          $('#submit_button').on('click', function(){

            var $name_val = $('#name_input').val()
            var $type_val = $('#type_input').val();
            var $age_val = $('#age_input').val();

            $.ajax({
              url: '/api/pets'.concat('?key=1111'),
              method: 'POST',
              contentType: 'application/json',
              data: JSON.stringify({"name": $name_val,
                                    "type": $type_val,
                                    "age": $age_val})
            }).done(function(data){
              $.ajax({
                url: '/pets',
                method: 'GET',

              }).done(function(data){
                $('body').html(data);
              });
            });
          });
        };
      });

      $('.pet_id').on('click', function(event){ //ZMIENIC NA KLIKANIE NA ID I POTEM WYBRAC CO SIE CHCE ZMIENIC I PRZESYLANIE ID W AJAX
    if($('#option_select').length == 0){

      var $clicked_id = $(this).text();

      var $option_select = $("<select>")
      .attr('id', 'option_select');

      var $name_option = $("<option value='name'>Imie</option>");
      var $type_option = $("<option value='type'>Gatunek</option>");
      var $age_option = $("<option value='age'>Wiek</option>");

      var $change_line = $('<input>')
      .attr('type', 'text')
      .attr('id', 'change_line');

      var $change_submit = $("<input>")
      .attr('type', 'button')
      .attr('id', 'change_submit')
      .attr('value', 'Zmień');

      $('#modify_container').append($option_select);
      $('#option_select').append($name_option);
      $('#option_select').append($type_option);
      $('#option_select').append($age_option)

      $('#modify_container').append($change_line);

      $('#modify_container').append($change_submit);

      $('#change_submit').on('click', function(){
        var $changed_attr = $('#option_select').val();
        var $changed_val = $('#change_line').val();

        var data_object = {};
        data_object[$changed_attr] = $changed_val;

        $.ajax({
          url: '/api/pets/'.concat($clicked_id, '?key=1111'),
          method: 'PATCH',
          data: JSON.stringify(data_object),
          contentType: 'application/json'
        }).done(function(data){
          $.ajax({
          url: '/pets',
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