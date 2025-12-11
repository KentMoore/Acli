// Data for the train schedule
var trainData = [
    {
        checi: "G101",
        fache: "北京南",
        daoda: "上海虹桥",
        fashi: "06:43",
        daoshi: "12:38",
        lishi: "05:55",
        shangwu: "¥1748.0",
        yideng: "¥933.0",
        erdeng: "¥553.0",
        ruanwo: "--",
        ruanzuo: "--",
        wuzuo: "--"
    },
    {
        checi: "G103",
        fache: "北京南",
        daoda: "上海虹桥",
        fashi: "06:53",
        daoshi: "12:48",
        lishi: "05:55",
        shangwu: "¥1748.0",
        yideng: "¥933.0",
        erdeng: "¥553.0",
        ruanwo: "--",
        ruanzuo: "--",
        wuzuo: "--"
    },
    {
        checi: "G105",
        fache: "北京南",
        daoda: "上海虹桥",
        fashi: "07:03",
        daoshi: "12:58",
        lishi: "05:55",
        shangwu: "¥1748.0",
        yideng: "¥933.0",
        erdeng: "¥553.0",
        ruanwo: "--",
        ruanzuo: "--",
        wuzuo: "--"
    },
    {
        checi: "G107",
        fache: "北京南",
        daoda: "上海虹桥",
        fashi: "07:13",
        daoshi: "13:08",
        lishi: "05:55",
        shangwu: "¥1748.0",
        yideng: "¥933.0",
        erdeng: "¥553.0",
        ruanwo: "--",
        ruanzuo: "--",
        wuzuo: "--"
    },
    {
        checi: "G109",
        fache: "北京南",
        daoda: "上海虹桥",
        fashi: "07:23",
        daoshi: "13:18",
        lishi: "05:55",
        shangwu: "¥1748.0",
        yideng: "¥933.0",
        erdeng: "¥553.0",
        ruanwo: "--",
        ruanzuo: "--",
        wuzuo: "--"
    }
];

var sortOrder = 1; // 1 for ascending, -1 for descending

// Main function called on body load
function changeColor() {
    initTopBar();
    initNav();
    initBanner();
    initWeek();
    initTable();
    initFooter();
}

// Initialize Top Bar
function initTopBar() {
    var topHtml =
        '<div id="top">' +
        '<div class="left">您好！欢迎来到我要回家网！ <a href="#">[登录]</a> <a href="#">[注册]</a></div>' +
        '<div class="right">' +
        '<ul>' +
        '<li><a href="#">我的订单</a> <span class="line">|</span></li>' +
        '<li><a href="#">支付方式</a> <span class="line">|</span></li>' +
        '<li class="list" onmouseover="showList()" onmouseout="hideList()">' +
        '<span>客户服务</span>' +
        '<div id="list_cur">' +
        '<a href="#">客户服务</a>' +
        '<a href="#">客户服务</a>' +
        '<a href="#">客户服务</a>' +
        '<a href="#">客户服务</a>' +
        '</div>' +
        '</li>' +
        '</ul>' +
        '</div>' +
        '</div>';
    document.getElementById("top_bg").innerHTML = topHtml;
}

// Show dropdown
function showList() {
    document.getElementById("list_cur").style.display = "block";
}

// Hide dropdown
function hideList() {
    document.getElementById("list_cur").style.display = "none";
}

// Initialize Navigation
function initNav() {
    var navHtml =
        '<div class="nav">' +
        '<h2><img src="images/logo.jpg" alt="Logo" /></h2>' +
        '<ul>' +
        '<li><a href="#">首页</a></li>' +
        '<li><a href="#">车票预订</a></li>' +
        '<li><a href="#">车票查询</a></li>' +
        '<li><a href="#">企业购票</a></li>' +
        '<li><a href="#">旅行服务</a></li>' +
        '</ul>' +
        '</div>';
    document.getElementById("nav_bg").innerHTML = navHtml;
}

// Initialize Banner
function initBanner() {
    document.getElementById("banner").innerHTML = '<img src="images/banner.jpg" alt="Banner" />';
}

// Initialize Week Tabs
function initWeek() {
    var weekHtml =
        '<li><a href="#" class="next">01-01<br>周一</a></li>' +
        '<li><a href="#">01-02<br>周二</a></li>' +
        '<li><a href="#">01-03<br>周三</a></li>' +
        '<li><a href="#">01-04<br>周四</a></li>' +
        '<li><a href="#">01-05<br>周五</a></li>' +
        '<li><a href="#">01-06<br>周六</a></li>' +
        '<li><a href="#">01-07<br>周日</a></li>';
    document.getElementById("week").innerHTML = weekHtml;
}

// Initialize Table
function initTable() {
    var tableHtml =
        '<tr class="title">' +
        '<td>车次</td>' +
        '<td>出发/到达站</td>' +
        '<td>出发/到达时间</td>' +
        '<td>历时</td>' +
        '<td onclick="sortTrainData(\'shangwu\')" style="cursor:pointer" title="点击排序">商务座 ↕</td>' +
        '<td onclick="sortTrainData(\'yideng\')" style="cursor:pointer" title="点击排序">一等座 ↕</td>' +
        '<td onclick="sortTrainData(\'erdeng\')" style="cursor:pointer" title="点击排序">二等座 ↕</td>' +
        '<td>软卧</td>' +
        '<td>软座</td>' +
        '<td>无座</td>' +
        '<td>操作</td>' +
        '</tr>';

    for (var i = 0; i < trainData.length; i++) {
        var rowClass = (i % 2 === 1) ? 'even' : '';
        var data = trainData[i];

        tableHtml += '<tr class="' + rowClass + '">' +
            '<td class="txt1">' + data.checi + '</td>' +
            '<td class="txt2">' +
            '<span class="red">始</span> ' + data.fache + '<br>' +
            '<span class="blue">终</span> ' + data.daoda +
            '</td>' +
            '<td class="txt2">' +
            data.fashi + '<br>' +
            data.daoshi +
            '</td>' +
            '<td>' + data.lishi + '</td>' +
            '<td class="colors">' + data.shangwu + '</td>' +
            '<td class="colors">' + data.yideng + '</td>' +
            '<td class="colors">' + data.erdeng + '</td>' +
            '<td>' + data.ruanwo + '</td>' +
            '<td>' + data.ruanzuo + '</td>' +
            '<td>' + data.wuzuo + '</td>' +
            '<td><a href="javascript:void(0)" onclick="bookTicket(\'' + data.checi + '\')" class="buy">预订</a></td>' +
            '</tr>';
    }

    document.getElementById("tbl").innerHTML = tableHtml;
}

// Sort function
function sortTrainData(key) {
    sortOrder *= -1;
    trainData.sort(function (a, b) {
        var valA = parseFloat(a[key].replace('¥', '')) || 0;
        var valB = parseFloat(b[key].replace('¥', '')) || 0;
        return (valA - valB) * sortOrder;
    });
    initTable();
}

// Booking function
function bookTicket(checi) {
    alert("您已成功预订 " + checi + " 次列车！\n祝您旅途愉快！");
}

// Initialize Footer
function initFooter() {
    document.getElementById("footer").innerHTML = 'Copyright &copy; 2017-2027 www.woyaohuijia.com All Rights Reserved | 京ICP备12345678号';
}
