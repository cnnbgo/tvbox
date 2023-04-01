var rule={
    title:'星辰',
    host:'http://www.40yb.com',
    url:'/fyclass/indexfypage.html[/fyclass/index.html]',
    searchUrl:'/search.php?page=fypage&searchword=**&searchtype=',
    searchable:2,//是否启用全局搜索,
    quickSearch:0,//是否启用快速搜索,
    filterable:0,//是否启用分类筛选,
    headers:{
        'User-Agent':'UC_UA',
        // "Cookie": ""
    },
    // class_parse:'.stui-header__menu li:gt(0):lt(7);a&&Text;a&&href;/(\\d+).html',
    class_parse:'.stui-header__menu li:gt(0):lt(7);a&&Text;a&&href;.*/(.*?)/.*html',
    play_parse:true,
    lazy:'',
    limit:6,
    推荐:'ul.stui-vodlist.clearfix;li;a&&title;.lazyload&&data-original;.pic-text&&Text;a&&href',
    double:true, // 推荐内容是否双层定位
    一级:'.stui-vodlist.clearfix&&li;a&&title;.lazyload&&data-original;.pic-text&&Text;a&&href',
    二级:{"title":"h1&&Text;.stui-content__detail p:eq(-2)&&Text","img":".lazyload&&data-original","desc":".stui-content__detail p:eq(0)&&Text;.stui-content__detail p:eq(1)&&Text;.stui-content__detail p:eq(2)&&Text","content":".detail&&Text","tabs":".stui-pannel__head&&h3","lists":".stui-content__playlist:eq(#id) li"},
    搜索:'ul.stui-vodlist__media:eq(0) li,ul.stui-vodlist:eq(0) li,#searchList li;a&&title;.lazyload&&data-original;.text-muted&&Text;a&&href;.text-muted:eq(-1)&&Text',
    搜索1:'ul.stui-vodlist&&li;a&&title;.lazyload&&data-original;.text-muted&&Text;a&&href;.text-muted:eq(-1)&&Text',
    搜索2:'ul.stui-vodlist__media&&li;a&&title;.lazyload&&data-original;.text-muted&&Text;a&&href;.text-muted:eq(-1)&&Text',
}