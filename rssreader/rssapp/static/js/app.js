const app = new Vue({
    el: '#app',
    delimiters: ['${', '}'],
    data: {
        channels: [],
        invox: [],
        user_id: window.localStorage['user_id'],
        request_data: null,
        channel_to_add: null,
        channel_to_delete: null
    },
    methods:{
        addChannelClick(channel){
            self = this;
            
            self.request_data = JSON.stringify({
                "addchannel": true,
                "model": "channel",
                "user_id": parseInt(self.user_id),
                "channel_id": channel.id
            });
            //alert(self.request_data);

            $.ajax({
                url: 'http://127.0.0.1:8000/api/crud/update/',
                contentType: "application/json",
                dataType: 'json',
                type: 'POST',
                data: self.request_data,
                success: function(result){
                    alert(result.data);
                    //console.log(result);
                },
                error: function(error) {
                   console.log(error);
                }
            });
        },
        removeChannelClick(channel){
            self = this;
            
            self.request_data = JSON.stringify({
                "model": "channel",
                "channel_id": channel.id,
                "deletechannel": true,
                "user_id": parseInt(self.user_id)
            });

            $.ajax({
                url: 'http://127.0.0.1:8000/api/crud/delete/',
                contentType: "application/json",
                dataType: 'json',
                type: 'POST',
                data: self.request_data,
                success: function(result){
                    alert(result.data);
                    //self.channels.pop(channel);
                    //console.log(result);
                },
                error: function(error) {
                   console.log(error);
                }
            });
        },
        getChannels(){
            self = this;
            self.request_data = JSON.stringify({ 
                "user_id": self.user_id
            });
            $.ajax({
                url: 'api/rss/chanles/users/',
                contentType: "application/json",
                dataType: 'json',
                type: 'POST',
                data: self.request_data,
                success: function(result){
                    self.channels = result.data;
                },
                error: function(error) {
                    console.log(error);
                }
            });
        }
    },
})