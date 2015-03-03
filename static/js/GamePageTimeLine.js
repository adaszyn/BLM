/**
 * Created by wojciech on 03.03.15.
 */
    $("#timeLine").bind('mousewheel', function(event) {
        if (event.originalEvent.wheelDelta >= 0) {
            timeLine.fillTheFirstOne();
        }
        else {
            timeLine.fillTheLastOne();
        }
    });
    timeLine = {

        //constructor
        init : function () {
          this.initialFill();
          var that = this;
            $(".timeLineElem").click(function (e) {
                $(".timeLineElem").css({'font-color' : 'white', 'font-weight' : 'normal'});
                $(e.target).css({'font-color' : '#c6ffe9', 'font-weight' : 'bold'});
               that.getGamesForDate($(e.target).text());
          });
        },

        //cached games for shifting
        cachedGames : [],

        //first element in timeline
        headElement : null,

        //timeLine carousel length
        length : 3,

        sortedGames : [],

        //DOM elements
        timelineElements : [
            $("#timeline1"),
            $("#timeline2"),
            $("#timeline3")
        ],

        //Dictionary of days where games took place
        gameDates : {},

        getGamesForDate : function (date) {

            $.get("/game/json/date="+date)
                    .done(function(data){
                        var games = JSON.parse(data);
                        $("#gamePaneBody").text('');
                        var gameStr = "";
                        for (var i = 0; i<games.length; i++){
                            gameStr += "<div class='well'><a href='"+ games[i]['url']+ "'>" + games[i]['away_team'] +'-'+ games[i]['home_team'] + ' </a>' +
                            "<span>" +  games[i]['away_score'] + " - " + games[i]['home_score'] + "</div>";
                        }
                        $("#gamePaneBody").append(gameStr);
                    })
                    .error(function(data){
                        console.log("Error while loading resources.");
                    });
        },

        updateGameDates : function (gd, dir) {

            if(Object.keys(gd).length === 0){       //no more dates to fill
                console.log('Could not find more games.');
                return;
            }
            if(this.headElement !== null){ //only if not initial fill
                if(dir === 1){ //right shift
                    this.headElement = this.timelineElements[1].text();
                }
                else{
                    this.headElement = Object.keys(gd)[0];
                }
            }
            for (var property in gd){
                if(gd.hasOwnProperty(property) === true){
                    this.gameDates[property] = gd[property];
                }
            }
            this.updateView();
        },
        updateView : function () {

            this.sortedGames = [];
            for (var property in this.gameDates){
                var obj = {
                    date :  property,
                    games : this.gameDates[property]
                };
                this.sortedGames.push(obj);
            }
            this.sortedGames.sort(function(a, b){
                if(new Date(a.date) > new Date(b.date)){
                    return 1;
                }
                else{
                    return -1;
                }
            });
            if(this.headElement === null) {
                this.headElement = this.sortedGames[0]['date']; //get first element of an array
            }
                var counter =0;
                for (var x=0;x<this.sortedGames.length; x++){
                    if(this.sortedGames[x]['date'] === this.headElement){
                        counter = x;
                        break;
                    }
                }

            this.timelineElements[0].text(this.sortedGames[counter].date);
            this.timelineElements[1].text(this.sortedGames[counter+1].date);
            this.timelineElements[2].text(this.sortedGames[counter+2].date);

        },
        getGames : function(date, limit, dir){
            var that = this;
            $.get("/game/json/date="+date+"&limitTo=" + limit + "&dir="+dir)
                .done(function (data) {
                    that.updateGameDates(JSON.parse(data), dir);
                })
                .error(function (data) {
                   console.log("Error during GET request. "+data);
                });
        },

        initialFill : function () {
            this.getGames('2014-06-10', 3, 1);
        },
        fillTheLastOne : function () {
            this.getGames(this.timelineElements[this.timelineElements.length-1].text(), 1, 1);
        },
        fillTheFirstOne : function () {
            this.getGames(this.timelineElements[0].text(), 1, 0);

        }

    };
timeLine.init();