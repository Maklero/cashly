import PropTypes from "prop-types";
import { BrowserRouter, Route, Switch } from "react-router-dom";

function Router({ routes }) {
    return (
        <BrowserRouter>
            <Switch>
                {routes.map(({ path, exact, component }, index) => (
                    <Route 
                        key={index}
                        path={path} 
                        exact={exact}
                        component={component} 
                    />
                ))}
            </Switch>
        </BrowserRouter>
    );
}

Router.propTypes = { routes: PropTypes.array.isRequired };

export default Router;