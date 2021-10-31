import { Redirect } from "react-router";
import { NotFound, Expenses, Categories } from "./pages"

const routes = [
    {
        path: "/",
        exact: true,
        component: () => <Redirect to="/expenses" />
    },
    {
        exact: true,
        path: "/expenses",
        component: Expenses
    },
    {
        exact: true,
        path: "/categories",
        component: Categories
    },
    {
        path: "*",
        component: NotFound
    }
];

export default routes;