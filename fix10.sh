cat << 'INNER_EOF' > /tmp/repl.txt
            start_node_service(frontend_path, "Frontend Client", args.frontend_port, api_url)
INNER_EOF
sed -i -e '/start_node_service(frontend_path, "Frontend Client", args.frontend_port, api_url), host):/r /tmp/repl.txt' -e '/start_node_service(frontend_path, "Frontend Client", args.frontend_port, api_url), host):/d' setup/services.py
