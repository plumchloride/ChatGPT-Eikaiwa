// 初期化、API等のデータ取得
$.get( './initialization').done(function( data ) {
  if(data["OpenAI_API_KYE"]){
    $("#OpenAI_API_KEY_status").text("API Key 設定済み");
    $("#OpenAI_API_KEY_status").css( 'background-color', '#9C99F2' );
  }else{
    $("#OpenAI_API_KEY_status").text("API Key 未設定");
    $("#OpenAI_API_KEY_status").css( 'background-color', '#ff5555' );
  };
});
// APIKey送信
$('#API_form').submit(function() {
  $.ajax({"type":"post","url":"./API_KEY","data":JSON.stringify({"key":$('#OpenAI_API_KEY').val()}),
          "contentType":'application/json',"dataType":"json",
          "success":function(json_data){
              if(json_data["SetAPI"]){
                $("#OpenAI_API_KEY_status").text("API Key 設定済み");
                $("#OpenAI_API_KEY_status").css( 'background-color', '#9C99F2' );
              }else{
                $("#OpenAI_API_KEY_status").text("API Key 未設定");
                $("#OpenAI_API_KEY_status").css( 'background-color', '#ff5555' );
              }
            },
          "error":function(){
            alert("Server Error. Please try again later.");
          }});
  $('#OpenAI_API_KEY').val("")
});
// 英語入力用のinputのサイズ制御
function flexTextarea(el) {
  const dummy = el.querySelector('.FlexTextarea__dummy')
  el.querySelector('.FlexTextarea__textarea').addEventListener('input', e => {
    dummy.textContent = e.target.value + '\u200b'
  })
}
document.querySelectorAll('.FlexTextarea').forEach(flexTextarea)
// 英語入力用のshiftenter挙動
$(document).on("keypress", "#FlexTextarea", function(e) {
  if (e.keyCode == 13 & e.shiftKey) { // shift + Enterが押された
    e.preventDefault();
    SendKaiwa()
  }
});

$text_area = $("#FlexTextarea")
text_sending = false
function SendKaiwa(){
  if(text_sending){
    $.noop()
  }else{
    text_sending = true
    if($text_area.val().replace(/\s+/g, '') != ""){
      var senddata = JSON.stringify({"text":$text_area.val()})
      $text_area.val("")
      $.ajax({"type":"post","url":"./EIKAIWA","data":senddata,
              "contentType":'application/json',"dataType":"json",
              "success":function(json_data){
                  console.log(json_data),
                  text_sending = false},
              "error":function(json_data){
                console.log(json_data)
                if(json_data["responseJSON"]["error"] == "API_ERROR"){
                  text_sending = false
                  alert("API Key が未入力もしくは間違っています。正しく入力して下さい");
                }else{
                  text_sending = false
                  alert("Server Error. Please try again later.");
                }
              }});
    }
  }
}