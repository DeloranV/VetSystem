$('#add_vet').on('click', function(){
      if($('#name_input').length == 0) {

        var $name_label = $('<label>Imie weterynarza</label>');
        var $name_input = $('<input>')
        .attr('id', 'name_input')
        .attr('type', 'text');

        var $surname_label = $('<label>Nazwisko weterynarza</label>');
        var $surname_input = $('<input>')
        .attr('id', 'surname_input')
        .attr('type', 'text');

        var $type_label = $('<label>Rodzaj wizyty</label>');
        var $type_select = $('<select>')
        .attr('id', 'type_select');

        var $kontrola_option = $('<option value="k">Kontrola</option>');
        var $zabieg_option = $('<option value="z">Zabieg</option>');
        var $dolegliwosc_option = $('<option value="d">Dolegliwość</option>');

        var $submit_button = $('<input>')
        .attr('type', 'button')
        .attr('id', 'submit_button')
        .attr('value', 'Zarejestruj');

        $('#add_vet_box').append($name_label, $name_input, $surname_label, $surname_input, $type_label,
                        $type_select, $submit_button);

        $('#type_select').append($kontrola_option, $zabieg_option, $dolegliwosc_option);

        $('#submit_button').on('click', function(){

          var $name_val = $('#name_input').val()
          var $surname_val = $('#surname_input').val();
          var $type_val = $('#type_select').val()

          $.ajax({
            url: '/api/vets'.concat('?key=1111'),
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({"name": $name_val,
                                  "surname": $surname_val,
                                  "appointment_type": $type_val})
          }).done(function(data){
            $.ajax({
              url: '/vets',
              method: 'GET',

            }).done(function(data){
              $('body').html(data);
            });
          });
        });
      };
    });

  $('#remove_vet').on('click', function(){
      var $vet_id = $('#remove_id').val();

      $.ajax({
        url: '/api/vets/'.concat($vet_id, '?key=1111'),
        method: 'DELETE'
      }).done(function(data){
        $.ajax({
          url: '/vets',
          method: 'GET'
        }).done(function(data){
          $('body').html(data);
        });
      });
    });

  $('.vet_id').on('click', function(event){ //ZMIENIC NA KLIKANIE NA ID I POTEM WYBRAC CO SIE CHCE ZMIENIC I PRZESYLANIE ID W AJAX
    if($('#option_select').length == 0){

      var $clicked_id = $(this).text();

      var $option_select = $("<select>")
      .attr('id', 'option_select');

      var $name_option = $("<option value='name'>Imie</option>");
      var $surname_option = $("<option value='type'>Nazwisko</option>");
      var $type_option = $("<option value='age'>Rodzaj wizyty</option>");

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
      $('#option_select').append($type_option)

      $('#modify_container').append($change_line);

      $('#modify_container').append($change_submit);

      $('#change_submit').on('click', function(){
        var $changed_attr = $('#option_select').val();
        var $changed_val = $('#change_line').val();

        var data_object = {};
        data_object[$changed_attr] = $changed_val;

        $.ajax({
          url: '/api/vets/'.concat($clicked_id, '?key=1111'),
          method: 'PATCH',
          data: JSON.stringify(data_object),
          contentType: 'application/json'
        }).done(function(data){
          $.ajax({
          url: '/vets',
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