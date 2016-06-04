var preflist = [];
var namedict = {};

$(function(){
  $.getJSON("preflist.json", function(json){
    preflist[0] = [];
    for(var i=1;i<=47;i++){
      var pref = japanmap_pref_code[i];
      preflist[i] = []
      $.each(json[pref], function(j, v){
        preflist[i].push(v.name);
        namedict[v.name] = v.json;
      });
      preflist[i].sort();
    }
  });
  mk_select($("select:first"));
  $("select:first").change(function(){
    if($(this).val() >= 1){
      $("#searchbtn").removeClass("ui-state-disabled");
      var t = $("select." + $(this).attr("class").replace(/ /g, "."));
      if(t.length == 1) append_select($(this), $("#pref-plus-end"), "か", $("#pref-plus-area"));
    }
    else $("#searchbtn").addClass("ui-state-disabled");
  });
  var t = $("select:last");
  mk_select(t);
  t.change(append_select_once(t, $("#pref-minus-end"), "や", $("#pref-minus-area")));

  $("#searchbtn").click(function(){
    var plus = [], minus = [];
    
    $("select.pref-plus").each(function(){
      var v = $(this).val() - 0;
      if(v) plus.push(v);
    });
    $("select.pref-minus").each(function(){
      var v = $(this).val() - 0;
      if(v) minus.push(v);
    });
    var plus_prefs_str = extract_to_prefs(plus).join("か");
    var minus_prefs_str = extract_to_prefs(minus).join("や");
    var prefs_str;
    if(minus_prefs_str.length){
      prefs_str = plus_prefs_str + "にあって、" + minus_prefs_str + "にない店：";
    }
    else{
      prefs_str = plus_prefs_str + "にある店：";
    }
    $("#query").text(prefs_str);
    var shops = get_shops(plus, minus);
    if(shops.length == 0){
      $("#list").text("見つかりませんでした。");
    }
    else{
      $("#list").text(shops.length + "件 見つかりました。");
      var ul = $("<ol>");
      for(i=0;i<shops.length;i++){
        ul.append($("<li>").append($("<a>").text(shops[i]).attr({
          "href": "shop.html#" + namedict[shops[i]],
          "rel": "external",
          "target": "_blank"})));
      }
      $("#list").append(ul);
    }
  });
  $("#resetbtn").click(function(){
    location.reload();
  });
}); 

function append_select_once(orig, pos, span_txt, create){
  var created = false;
  
  function f(){
    if(!created){
      append_select(orig, pos, span_txt, create);
      created = true;
    }
  }
  return f;
}
function append_select(orig, pos, span_txt, create){
  var sel = orig.clone();
  sel.insertBefore(pos);
  $("<span>").text(span_txt).insertBefore(sel);
  create.trigger("create");
  sel.change(append_select_once(orig, pos, span_txt, create));
  return sel;
}

function mk_select(jq){
  jq.append($("<option>").val(0).text("選択してください"));
  for(i=1;i<=47;i++){
    jq.append($("<option>").val(i).text(japanmap_pref_code[i]));
  }
  return jq
}


/** JQueryとかDOMとか出てこないところ **/

function extract_to_prefs(li){
  var ret = [];
  for(var i=0;i<li.length;i++){
    if(li[i] - 0){
      var pref = japanmap_pref_code[li[i]];
      if(ret.indexOf(pref) == -1) ret.push(pref);
    }
  }
  return ret;
}

function get_shops(plus, minus){
  if(plus.length == 0) return [];
  var all_plus = [].concat(preflist[plus[0]]);
  for(var i=1;i<plus.length;i++) union_to(all_plus, preflist[plus[i]]);
  if(minus.length == 0) return all_plus;
  var all_minus = [].concat(preflist[minus[0]]);
  for(var i=1;i<minus.length;i++) union_to(all_minus, preflist[minus[i]]);
  return mk_sub(all_plus, all_minus);
}

/** prefとかすら出てこないところ **/

function union_to(lhs, rhs){
  var i, j, lhs_len = lhs.length;
  for(i=0,j=0;i<lhs_len&&j<rhs.length;){
    if(lhs[i] < rhs[j]) i++;
    else{
      lhs[i] != rhs[j] ? lhs.push(rhs[j]) : i++;
      j++;
    }
  }
  for(;j<rhs.length;j++) lhs.push(rhs[j]);
  lhs.sort();
  return lhs;
}

function mk_sub(lhs, rhs){
  var i, j, a = [];

  for(i=0,j=0;i<lhs.length&&j<rhs.length;){
    if(lhs[i] < rhs[j]){
      a.push(lhs[i]);
      i++;
    }
    else{
      if(lhs[i] == rhs[j]) i++;
      j++;
    }
  }
  for(;i<lhs.length;i++) a.push(lhs[i]);
  return a;
}
