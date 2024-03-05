```mermaid.js
graph LR
  subgraph Discord Bot [MyClient]
    MyClient --> on_ready
    on_ready --> [Logins to Discord]
    on_ready --> |Success?| checks_channel_id
    checks_channel_id --> [Channel Found]
    checks_channel_id --> |Channel not found!| print_error_message
    Channel Found --> loads_allowed_licenses
    Channel Found --> on_message
    loads_allowed_licenses --> on_member_join
    on_member_join --> [New Member Joined] --> welcome_channel_check
    welcome_channel_check --> [Welcome Channel Found] --> send_welcome_message
    welcome_channel_check --> |Welcome Channel not found!| print_error_message
    send_welcome_message --> |Message Sent|
    on_message --> |Is message from Bot?| is_message_from_bot
    is_message_from_bot --> |Yes| 
    is_message_from_bot --> |No| starts_with_exclamation_mark
    starts_with_exclamation_mark --> |Yes| extracts_command
    starts_with_exclamation_mark --> |No| 
    extracts_command --> handles_command
    handles_command --> |!help| send_help_message
    handles_command --> |!hallo| send_hallo_message
    handles_command --> |!roles| show_roles
    handles_command --> |!removeRoles| remove_roles
    handles_command --> |!apod| send_apod_message  
    handles_command --> |!joke| get_joke
    handles_command --> |other message| print_message_to_console
    send_help_message --> |Help Sent|
    send_hallo_message --> |Message Sent|
    show_roles --> [RoleCommandHandler.show_roles]
    remove_roles --> [RoleCommandHandler.remove_roles]
    send_apod_message --> |Currently Disabled| print_error_message
    get_joke --> [Jokes.get_joke]
    get_joke --> |Joke Retrieved| send_joke_message
    send_joke_message --> |Joke Sent|
    print_message_to_console --> |Message Printed|
    on_interaction --> |Interaction Type?| checks_interaction_type
    checks_interaction_type --> |Button Interaction| handle_button_interaction
    handle_button_interaction --> |Checks custom_id| begins_with_add_or_remove
    begins_with_add_or_remove --> |StartsWith add_| get_role_and_add
    begins_with_add_or_remove --> |StartsWith remove_| get_role_and_remove
    get_role_and_add --> |Role Retrieved| add_role_to_user
    get_role_and_remove --> |Role Retrieved| remove_role_from_user
    add_role_to_user --> |Role Added| send_role_add_message
    remove_role_from_user --> |Role Removed| send_role_remove_message
    send_role_add_message --> |Message Sent|
    send_role_remove_message --> |Message Sent|
    MyClient --> on_close
    on_close --> |Success?| checks_channel_id_for_close
    checks_channel_id_for_close --> |Channel Found| send_goodbye_message
    checks_channel_id_for_close --> |Channel not found!| 
    send_goodbye_message --> |Message Sent|
  subgraph NASA API [NASA]
    NASA --> get_apod
    get_apod --> |API Request| checks_status_code
    checks_status_code --> |Success (200)| extracts_data
    checks_status_code --> |Failed| print_error_message
    extracts_data --> |Data Extracted| sends_apod_info
    sends_apod_info --> |Message Sent|
  subgraph Joke API [Jokes]
    Jokes --> get_joke
    get_joke --> |API Request| checks_status_code
    checks_status_code --> |Success (200)| extracts_joke
    checks_status_code --> |Failed| print_error_message
    extracts_joke --> |Joke Extracted| sends_joke
    sends_joke --> |Message Sent|
  subgraph Role Handler [RoleCommandHandler]
    RoleCommandHandler --> show_roles
    show_roles --> |Gets Roles| checks_for_roles

```
