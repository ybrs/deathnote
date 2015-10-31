$(function(){
    var postDeath = function(_data){
          $.ajax({
              type: "POST",
              url: '/',
              data: _data,
              complete: function(){
                  location.reload()
              },
              dataType : "json",
              contentType: "application/json; charset=utf-8",
            });
    };


    $('.death-input').keypress(function (e) {
      var _data = JSON.stringify({text: $('.death-input').val()});
      if (e.which == 13) {
            postDeath(_data)
        return false;    //<---- Add this line
      }
    });
    $('.list-group-item-text').on('click', function(element){
        _data = JSON.stringify({text: $(element.target).html()})
        postDeath(_data)
    })

})