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

# Summarizes a Youtube Video - Disabled Due to LLM Limitations 
@bot.slash_command(guilds=scope, description="Uses /Ask_Alt and scraped video captions to summarize the video")
async def summarize_video(ctx: ApplicationContext, url: Option(str, "The url of the video to summarize", required=True)):
    await ctx.defer()
    summary: list = await summarizer.summarize(url)

    for chunk in summary:
        await ctx.followup.send(chunk)
        time.sleep(0.25)