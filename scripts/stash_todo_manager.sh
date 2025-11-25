#!/bin/bash
# Human-in-the-loop Todo List for Resolving Unpushed Stashes
# This script creates a structured workflow for managing stashes with manual review

set -e

# Source common library to avoid code duplication
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMMON_LIB="$SCRIPT_DIR/lib/stash_common.sh"

if [[ -f "$COMMON_LIB" ]]; then
    source "$COMMON_LIB"
else
    echo "Error: Common library not found at $COMMON_LIB"
    exit 1
fi

# Configuration
TODO_FILE="/tmp/stash_resolution_todo_$$"
BACKUP_DIR="$HOME/.stash_resolution_backups"
mkdir -p "$BACKUP_DIR"

# Function to display help
show_help() {
    print_color "BLUE" "Human-in-the-loop Stash Resolution Todo Manager"
    echo "Usage: $0 [command] [options]"
    echo ""
    echo "Commands:"
    echo "  init                    Initialize todo list with unpushed stashes"
    echo "  list                    List current todo items"
    echo "  show <item_id>          Show details of a todo item"
    echo "  resolve <item_id>       Resolve a specific todo item interactively"
    echo "  skip <item_id>          Skip a todo item (mark as done without action)"
    echo "  remove <item_id>        Remove a todo item from the list"
    echo "  status                  Show resolution progress"
    echo "  export <file>           Export todo list to a file"
    echo "  import <file>           Import todo list from a file"
    echo "  reset                   Reset todo list and start over"
    echo "  help                    Show this help message"
    echo ""
    echo "Workflow:"
    echo "  1. Run 'init' to create todo list from unpushed stashes"
    echo "  2. Use 'list' to see items needing resolution"
    echo "  3. Use 'resolve <id>' to work on specific items"
    echo "  4. Use 'status' to track progress"
    echo ""
    echo "Examples:"
    echo "  $0 init"
    echo "  $0 list"
    echo "  $0 resolve 1"
    echo "  $0 status"
}

# Function to get unpushed stashes
get_unpushed_stashes() {
    # Get all stashes
    local all_stashes
    readarray -t all_stashes < <(git stash list | cut -d: -f1)
    
    # For each stash, check if it's been pushed
    local unpushed=()
    for stash in "${all_stashes[@]}"; do
        if [[ -n "$stash" ]]; then
            # Check if stash has been pushed (this is a simplified check)
            # In a real implementation, we'd need to check against remote branches
            unpushed+=("$stash")
        fi
    done
    
    printf '%s\n' "${unpushed[@]}"
}

# Function to initialize todo list
init_todo_list() {
    print_color "BLUE" "Initializing todo list with unpushed stashes..."
    
    # Clear existing todo file
    > "$TODO_FILE"
    
    # Get unpushed stashes
    local stashes
    readarray -t stashes < <(get_unpushed_stashes)
    
    if [[ ${#stashes[@]} -eq 0 ]]; then
        print_color "GREEN" "No unpushed stashes found"
        return 0
    fi
    
    print_color "BLUE" "Found ${#stashes[@]} unpushed stashes:"
    
    local id=1
    for stash in "${stashes[@]}"; do
        if [[ -n "$stash" ]]; then
            local stash_message=$(git stash list | grep "$stash" | cut -d: -f2-)
            local branch_name=$(get_branch_from_stash "$stash_message")
            
            # Add to todo list (status: pending)
            echo "$id|$stash|$branch_name|$stash_message|pending" >> "$TODO_FILE"
            
            printf "  %d) %s (%s) - %s\n" "$id" "$stash" "$branch_name" "$stash_message"
            ((id++))
        fi
    done
    
    print_color "GREEN" "Todo list initialized with $id items"
    print_color "YELLOW" "Use 'list' to see items or 'resolve <id>' to start working"
}

# Function to list todo items
list_todo_items() {
    if [[ ! -f "$TODO_FILE" ]] || [[ ! -s "$TODO_FILE" ]]; then
        print_color "YELLOW" "Todo list is empty. Run 'init' to populate it."
        return 0
    fi
    
    print_color "BLUE" "Stash Resolution Todo List:"
    echo "ID | Status   | Stash Ref        | Branch        | Description"
    echo "---|----------|------------------|---------------|------------"
    
    while IFS='|' read -r id stash_ref branch message status; do
        local status_color="BLUE"
        case "$status" in
            "pending") status_color="YELLOW" ;;
            "resolved") status_color="GREEN" ;;
            "skipped") status_color="CYAN" ;;
            *) status_color="RED" ;;
        esac
        
        printf "%-2s | " "$id"
        print_color "$status_color" "$(printf "%-8s" "$status")"
        printf " | %-16s | %-13s | %s\n" "$stash_ref" "$branch" "$message"
    done < "$TODO_FILE"
}

# Function to show details of a todo item
show_todo_item() {
    local item_id="$1"
    
    if [[ -z "$item_id" ]]; then
        print_color "RED" "Error: Item ID required"
        return 1
    fi
    
    if [[ ! -f "$TODO_FILE" ]]; then
        print_color "RED" "Error: Todo list not initialized"
        return 1
    fi
    
    local item_line=$(grep "^$item_id|" "$TODO_FILE")
    if [[ -z "$item_line" ]]; then
        print_color "RED" "Error: Item $item_id not found"
        return 1
    fi
    
    IFS='|' read -r id stash_ref branch message status <<< "$item_line"
    
    print_color "BLUE" "Todo Item Details:"
    echo "ID: $id"
    echo "Status: $status"
    echo "Stash Ref: $stash_ref"
    echo "Branch: $branch"
    echo "Description: $message"
    echo ""
    
    # Show stash contents
    print_color "BLUE" "Stash Contents:"
    git stash show -p "$stash_ref" 2>/dev/null | head -20
    echo "..."
}

# Function to resolve a todo item
resolve_todo_item() {
    local item_id="$1"
    
    if [[ -z "$item_id" ]]; then
        print_color "RED" "Error: Item ID required"
        return 1
    fi
    
    if [[ ! -f "$TODO_FILE" ]]; then
        print_color "RED" "Error: Todo list not initialized"
        return 1
    fi
    
    local item_line=$(grep "^$item_id|" "$TODO_FILE")
    if [[ -z "$item_line" ]]; then
        print_color "RED" "Error: Item $item_id not found"
        return 1
    fi
    
    IFS='|' read -r id stash_ref branch message status <<< "$item_line"
    
    if [[ "$status" != "pending" ]]; then
        print_color "YELLOW" "Item $item_id is already marked as $status"
        return 0
    fi
    
    print_color "BLUE" "Resolving stash: $stash_ref"
    echo "Branch: $branch"
    echo "Description: $message"
    echo ""
    
    # Show stash details
    print_color "BLUE" "Stash Details:"
    git stash show -p "$stash_ref" | head -10
    echo "..."
    echo ""
    
    # Ask user what to do
    print_color "YELLOW" "How would you like to resolve this stash?"
    echo "1) Apply interactively (resolve conflicts)"
    echo "2) Apply without conflicts (if possible)"
    echo "3) Drop the stash"
    echo "4) Save to branch and push"
    echo "5) Skip for now"
    echo "6) Cancel"
    echo -n "Enter your choice (1-6): "
    
    read -r choice
    
    case $choice in
        1)
            # Apply with interactive resolution
            print_color "BLUE" "Applying stash interactively..."
            local resolver_script="$SCRIPT_DIR/interactive_stash_resolver_optimized.sh"
            if [[ -f "$resolver_script" ]]; then
                if "$resolver_script" "$stash_ref"; then
                # Mark as resolved - use proper field matching
                sed -i "/^${id}\|/s/|pending$|/|resolved|/" "$TODO_FILE"
                print_color "GREEN" "Stash resolved successfully"
                    
                    # Ask if user wants to drop the stash
                    if confirm_action "Drop the stash now?"; then
                        git stash drop "$stash_ref"
                        print_color "GREEN" "Stash dropped"
                    fi
                else
                    print_color "RED" "Failed to resolve stash"
                fi
            else
                print_color "RED" "Interactive resolver not found"
                return 1
            fi
            ;;
        2)
            # Apply without conflicts
            print_color "BLUE" "Applying stash..."
            if git stash apply "$stash_ref"; then
            # Mark as resolved - use proper field matching
            sed -i "/^${id}\|/s/|pending$|/|resolved|/" "$TODO_FILE"
            print_color "GREEN" "Stash applied successfully"
                
                # Add all changes
                git add -A
                
                # Ask if user wants to drop the stash
                if confirm_action "Drop the stash now?"; then
                    git stash drop "$stash_ref"
                    print_color "GREEN" "Stash dropped"
                fi
            else
                print_color "RED" "Failed to apply stash (conflicts detected)"
                print_color "YELLOW" "Try interactive resolution instead"
            fi
            ;;
        3)
        # Drop the stash
        if confirm_action "Are you sure you want to drop $stash_ref?"; then
        git stash drop "$stash_ref"
        # Mark as resolved - use proper field matching
        sed -i "/^${id}\|/s/|pending$|/|resolved|/" "$TODO_FILE"
        print_color "GREEN" "Stash dropped"
            else
                print_color "BLUE" "Operation cancelled"
            fi
            ;;
        4)
            # Save to branch and push
            print_color "BLUE" "Creating branch for stash..."
            local new_branch="stash-resolve-$(date +%Y%m%d-%H%M%S)"
            git checkout -b "$new_branch"
            
            if git stash apply "$stash_ref"; then
            git add -A
            git commit -m "Apply stash: $message"
            print_color "GREEN" "Changes committed to branch $new_branch"
            print_color "YELLOW" "Remember to push and merge when ready"
            
            # Mark as resolved - use proper field matching
            sed -i "/^${id}\|/s/|pending$|/|resolved|/" "$TODO_FILE"
            else
                print_color "RED" "Failed to apply stash"
                git checkout -
                git branch -D "$new_branch"
            fi
            ;;
        5)
            print_color "BLUE" "Skipping item for now"
            ;;
        6)
            print_color "BLUE" "Operation cancelled"
            ;;
        *)
            print_color "RED" "Invalid choice"
            return 1
            ;;
    esac
}

# Function to skip a todo item
skip_todo_item() {
    local item_id="$1"
    
    if [[ -z "$item_id" ]]; then
        print_color "RED" "Error: Item ID required"
        return 1
    fi
    
    if [[ ! -f "$TODO_FILE" ]]; then
        print_color "RED" "Error: Todo list not initialized"
        return 1
    fi
    
    local item_line=$(grep "^$item_id|" "$TODO_FILE")
    if [[ -z "$item_line" ]]; then
        print_color "RED" "Error: Item $item_id not found"
        return 1
    fi
    
    IFS='|' read -r id stash_ref branch message status <<< "$item_line"
    
    if [[ "$status" == "skipped" ]]; then
        print_color "YELLOW" "Item $item_id is already marked as skipped"
        return 0
    fi
    
    # Mark as skipped - use proper field matching
    sed -i "/^${id}\|/s/|pending$|/|skipped|/" "$TODO_FILE"
    print_color "GREEN" "Item $item_id marked as skipped"
}

# Function to remove a todo item
remove_todo_item() {
    local item_id="$1"
    
    if [[ -z "$item_id" ]]; then
        print_color "RED" "Error: Item ID required"
        return 1
    fi
    
    if [[ ! -f "$TODO_FILE" ]]; then
        print_color "RED" "Error: Todo list not initialized"
        return 1
    fi
    
    local item_line=$(grep "^$item_id|" "$TODO_FILE")
    if [[ -z "$item_line" ]]; then
        print_color "RED" "Error: Item $item_id not found"
        return 1
    fi
    
    # Remove from todo list
    sed -i "/^$item_id|/d" "$TODO_FILE"
    print_color "GREEN" "Item $item_id removed from todo list"
}

# Function to show resolution status
show_status() {
    if [[ ! -f "$TODO_FILE" ]] || [[ ! -s "$TODO_FILE" ]]; then
        print_color "YELLOW" "Todo list is empty"
        return 0
    fi
    
    local total=$(wc -l < "$TODO_FILE")
    local resolved=$(grep -c "|resolved$" "$TODO_FILE" || echo 0)
    local skipped=$(grep -c "|skipped$" "$TODO_FILE" || echo 0)
    local pending=$((total - resolved - skipped))
    
    print_color "BLUE" "Stash Resolution Status:"
    echo "Total items: $total"
    print_color "GREEN" "Resolved: $resolved"
    print_color "YELLOW" "Pending: $pending"
    print_color "CYAN" "Skipped: $skipped"
    
    if [[ $total -gt 0 ]]; then
        local percent=$((resolved * 100 / total))
        echo "Progress: $percent%"
    fi
}

# Function to export todo list
export_todo_list() {
    local export_file="$1"
    
    if [[ -z "$export_file" ]]; then
        print_color "RED" "Error: Export file required"
        return 1
    fi
    
    if [[ ! -f "$TODO_FILE" ]]; then
        print_color "RED" "Error: Todo list not initialized"
        return 1
    fi
    
    cp "$TODO_FILE" "$export_file"
    print_color "GREEN" "Todo list exported to $export_file"
}

# Function to import todo list
import_todo_list() {
    local import_file="$1"
    
    if [[ -z "$import_file" ]]; then
        print_color "RED" "Error: Import file required"
        return 1
    fi
    
    if [[ ! -f "$import_file" ]]; then
        print_color "RED" "Error: Import file not found"
        return 1
    fi
    
    cp "$import_file" "$TODO_FILE"
    print_color "GREEN" "Todo list imported from $import_file"
}

# Function to reset todo list
reset_todo_list() {
    if confirm_action "Are you sure you want to reset the todo list?"; then
        rm -f "$TODO_FILE"
        print_color "GREEN" "Todo list reset"
    else
        print_color "BLUE" "Operation cancelled"
    fi
}

# Main execution
main() {
    case "$1" in
        init)
            init_todo_list
            ;;
        list)
            list_todo_items
            ;;
        show)
            show_todo_item "$2"
            ;;
        resolve)
            resolve_todo_item "$2"
            ;;
        skip)
            skip_todo_item "$2"
            ;;
        remove)
            remove_todo_item "$2"
            ;;
        status)
            show_status
            ;;
        export)
            export_todo_list "$2"
            ;;
        import)
            import_todo_list "$2"
            ;;
        reset)
            reset_todo_list
            ;;
        help|--help|-h)
            show_help
            ;;
        "")
            show_help
            ;;
        *)
            print_color "RED" "Unknown command: $1"
            show_help
            exit 1
            ;;
    esac
}

# Cleanup function
cleanup() {
    # Backup todo file on exit
    if [[ -f "$TODO_FILE" ]]; then
        cp "$TODO_FILE" "$BACKUP_DIR/stash_todo_$(date +%Y%m%d_%H%M%S).bak" 2>/dev/null || true
    fi
}

# Set up cleanup trap
trap cleanup EXIT

# Run main function with all arguments
main "$@"