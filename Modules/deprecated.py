# Sends Weather Report
async def send_weather_report(user_id: str, location: str):
    user = await bot.fetch_user(user_id)
    report = await get_current_report(location)
    await user.send(report)

# Provides the User with a Report on their Local Weather (If Configured) 
@bot.slash_command(guild=scope, description="Opt in for a daily weather report of your City")
async def daily_weather(ctx: ApplicationContext,
                  city : Option(str, "The Name of the City to Report", required=True),
                  time_zone: Option(str, "Your Time Zone", choices=["Pacific", "Mountain", "Central", "Eastern"], required=True),
                  report_time: Option(int, "what hour would you Like to Recieve The Report 1-24", min_value=1,  max_value=24),
                  stop_reports: Option(bool, "set this to true to cancel weather notifications", required=False),
                  ):
    # Get User Object (Creates New if It Doesn't Exist)
    user = await get_user(ctx, user_list)
    
    if stop_reports:
        user.set_location(None)
    else:
        # Format Correctly
        location = city.strip().replace(" ", "+")
        
        # Schedule Time
        report_time = convert_to_pacific(time_zone, report_time)
        
        # Update User Object
        user.set_location(location)
        user.set_report_time(report_time)
        # Register New Scheduler
        scheduler.add_job(func=send_weather_report, args=[user.id, user.location], trigger='cron', hour=user.report_time)
    
    await ctx.respond(random.choice(sarcastic_responses), ephemeral=True)


class llama:
    
    def __init__(self):
        self.queue = []
        self.api_endpoint = "http://localhost:5000/api/v1/generate"
        
        
    async def generate(self, query: str, max_tokens: int = 2048, min_length: int = 0, include_query: bool = True, raw_response: bool = False):
                
        params = {
            'prompt': query,
            'max_new_tokens': max_tokens,
            'do_sample': True,
            'temperature': 1.31,
            'top_p': 0.14,
            'typical_p': 1,
            'repetition_penalty': 1.18,
            'encoder_repetition_penalty': 1.0,
            'top_k': 50,
            'min_length': min_length,
            'no_repeat_ngram_size': 0,
            'num_beams': 1,
            'penalty_alpha': 0,
            'length_penalty': 1,
            'early_stopping': False,
            'seed': -1,
            'add_bos_token': True,
            'truncation_length': 2048,
            'ban_eos_token': False,
            'skip_special_tokens': True,
            'stopping_strings': [],
        }
        
        try:
            # Send Request
            async with aiohttp.ClientSession() as session:
                async with session.post(url=self.api_endpoint, json=params) as response:
                    res = await response.json()

                    # Respond With Input Parameters Included
                    response_message = str(res['results'][0]['text'])
                    response_message.replace("`", "")

                    log_entry = {"date": datetime.now().isoformat(), "query": query, "response" : response_message }
                    with open("Logs/LLaMa.json", 'a') as log:
                        json.dump(log_entry, log)
                        log.write(os.linesep)
                    
                    if raw_response:
                        return response_message
                    
                    # Only Respond     
                    formatted = ''.join([''.join(["> ", i.strip(), "\n"]) for i in response_message.strip().split("\n")])
                    if include_query:
                        return f"{query}\n{formatted}"
                    else:
                        return f"{formatted}"
                    
        except Exception as e:
            return f"Error : {e}"
