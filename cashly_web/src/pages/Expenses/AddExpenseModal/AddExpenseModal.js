import { useMutation, useQueryClient } from "react-query";
import NiceModal, { useModal, bootstrapDialog } from "@ebay/nice-modal-react";

import { createExpense } from "../../../mutations";
import ExpenseModal from "../ExpenseModal/ExpenseModal";


export default NiceModal.create(() => {
    const modal = useModal();
    const queryClient = useQueryClient();
    
    const initialValues = { amount: 0, categoryId: "" };

    const mutation = useMutation(createExpense, {
        onSuccess: () => {
            modal.hide();
            queryClient.invalidateQueries("expenses");
        }
    });

    const onSubmit = (values, { resetForm }) => {
        resetForm();
        mutation.mutate(values);
    };

    return (
        <ExpenseModal 
            {...bootstrapDialog(modal)}
            submitText="Dodaj"
            title="Dodaj wydatek"
            onSubmit={onSubmit}
            initialValues={initialValues}
            description={`
                Lorem ipsum dolor sit amet, 
                consectetur adipiscing elit, 
                sed do eiusmod tempor incididunt.
            `}
        />
    );
});