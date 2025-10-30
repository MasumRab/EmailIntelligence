import { Route, Switch } from "wouter";
import Dashboard from "@/pages/dashboard";
import LoginPage from "@/pages/login";
import ProfilePage from "@/pages/profile";

export default function App() {
  return (
    <Switch>
      <Route path="/" component={Dashboard} />
      <Route path="/login" component={LoginPage} />
      <Route path="/profile" component={ProfilePage} />
      <Route>
        {/* Default route */}
        <Dashboard />
      </Route>
    </Switch>
  );
}