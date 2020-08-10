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
            
            params = JSON.stringify({
                "addchannel": true,
                "user_id": parseInt(self.user_id),
                "channel_id": channel.id
            });
            //alert(self.request_data);

            $.ajax({
                url: 'http://127.0.0.1:8000/api/channel/update/',
                contentType: "application/json",
                dataType: 'json',
                type: 'POST',
                data: params,
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
            params = null;
            
            params = JSON.stringify({
                "channel_id": channel.id,
                "user_id": parseInt(self.user_id)
            });

            $.ajax({
                url: 'http://127.0.0.1:8000/api/channel/delete/',
                contentType: "application/json",
                dataType: 'json',
                type: 'POST',
                data: params,
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
            params = JSON.stringify({ 
                "user_id": self.user_id
            });

            $.ajax({
                url: 'http://127.0.0.1:8000/api/rss/channels/users/',
                contentType: "application/json",
                dataType: 'json',
                type: 'POST',
                data: params,
                success: function(result){
                    console.log(result);
                    self.channels = result.data;
                },
                error: function(error) {
                    console.log(error);
                }
            });
        },
        sync_channels(){
            self = this;
            
            fetch('http://127.0.0.1:8000/api/rss/channels/datasource/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ 
                    "user_id": parseInt(self.user_id),
                    "async":true,
                })
            })
            .then(response => response.json())
            .then(data => {
                data.forEach(el => self.invox.push(el));
                console.log(data);
            })
            .catch(function(error) {
                console.log(error);
            });
            
        }
    },
    mounted() {
        setInterval(this.sync_channels, 10000);
    }
})