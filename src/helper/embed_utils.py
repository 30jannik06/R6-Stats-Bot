import discord

def create_embed(
    title: str,
    description: str,
    fields: list = None,
    color: discord.Color = discord.Color.from_rgb(255,255,255),
    footer_text: str = None,
    footer_icon_url: str = None,
    thumbnail_url: str = None,
    image_url: str = None,
    author_name: str = None,
    author_icon_url: str = None,
    timestamp: bool = False,
    
) -> discord.Embed:
    '''
    Created a Discord Embed with the given parameters.
    
    :param title: The title of the embed.
    :param description: The description text of the embed.
    :param fields: A list of dictionaries, each containing "name", "value", and optionally "inline".
    :param color: The color of the embed. Defaults to RGB White.
    :param footer_text: The text for the footer of the embed.
    :param footer_icon_url: The icon URL for the footer.
    :param thumbnail_url: The URL of the thumbnail image.
    :param image_url: The URL of the main image.
    :param author_name: The name of the author to display at the top.
    :param author_icon_url: The URL of the author`s icon.
    :param timestamp: If True, add the current timestamp to the embed.
    :return: A discord.Embed object
    '''
    
    embed = discord.Embed(title=title, description=description, color=color)
    
    if footer_text:
        embed.set_footer(text=footer_text, icon_url=footer_icon_url)
        
    if thumbnail_url:
        embed.set_thumbnail(url=thumbnail_url)
    
    if image_url:
        embed.set_image(url=image_url)
        
    if author_name:
        embed.set_author(name=author_name, icon_url=author_icon_url)
    
    if fields:
        for field in fields:
            embed.add_field(name=field["name"], value=field["value"], inline=field.get("inline", False))
            
    if timestamp:
        embed.timestamp = discord.utils.utcnow()
        
    return embed