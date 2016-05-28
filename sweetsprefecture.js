var map_width;
function shopdataFromJson(jsonurl){
  var div = $("<div>");

  $.getJSON(jsonurl, function(json){
    var detail = $("<div>");
    var map = $("<div>");
    var anchor = $("<h1>");
    if(json.url.constructor !== Array){
      anchor.append($("<a>").attr("href", json.url).text(json.name));
    }
    else{
      anchor.text(json.name);
      var small = $("<sub>");
      for(var i=0;i<json.url.length;i++){
        small.append(" [");
        small.append($("<a>").attr("href", json.url[i]).text(i+1));
        small.append("]");
      }
      anchor.append(small);
    }
    div.append(anchor.attr("name", json.name));

    for(var i=1;i<=48;i++){
      var pref = japanmap_pref_code[i];
      if(!(pref in json.shops)) continue;
      detail.append($("<h2>").attr("id", pref).text(pref));
      var dl = $("<dl>");
      $.each(json.shops[pref], function(i, v){
        dl.append($("<dt>").text(v.name));
        dl.append($("<dd>").text(v.address));
      });
      detail.append(dl);
    }
    var available = [];
    var not_available = [];
    for(var i=1;i<=47;i++){
      (japanmap_pref_code[i] in json.shops ? available : not_available).push(i);
    }
    var areas = [{"code": 1, "name": "店あり", "color": "#ff0000", "prefectures": available},
      {"code": 2, "name": "店なし", "prefectures": not_available}];
    map.japanMap({width: map_width, movesIslands: true, areas: areas,
      onSelect: function(data){
        if(data.area.name == "店あり"){
          scrollTo(0, $("#" + data.name).offset().top);
        }
      }
    });
    div.append(map).append(detail);
    var tail = $("<div>");
    tail.text("最終確認日: " + (new Date(json.lastChecked.date)).toLocaleString());
    if(json.lastChecked.status != "OK"){
      tail.text(tail.text() + "　" +
            "一部、取得に失敗している可能性があります。 (status=" + json.lastChecked.status + ")");
    }
    div.append(tail);
  });
  return div;
}

$(function(){
  var shoplist = $("#shop");
  var elem = $("#main");
  map_width = screen.width - 30 < 400 ? screen.width - 30 : 400;

  $.getJSON("shoplist.json", function(json){
    $.each(json, function(i, shop){
      shoplist.append($("<option>").text(shop.name).val(shop.json));
    });
  });
  shoplist.change(function(){
    elem.empty();
    elem.append(shopdataFromJson($(this).val()));
  });

  $("#goto-top").click(function(){
    scrollTo(0, 0);
  });
});
