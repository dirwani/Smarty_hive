import { useEffect, useState } from "react";
import { fetchAssignments, deleteAssignments } from "../../services/Forum/forum";
import ToastMessage from "../../utils/toaster/toaster";
import Assignment from "../../components/Assignment/assignment";

export function AssignmentRoute() {
    const [assignments, setAssignments] = useState([]);

    useEffect(() => {
        async function fetchData() {
            try {
                const response = await fetchAssignments();
                setAssignments(response);
            } catch (error) {
                ToastMessage.error("Failed to fetch assignments.");
                console.error(error);
            }
        }

        fetchData();
    }, []);


    const handleAssignmentDelete = (id) => {
        try {
            deleteAssignments(id)
            ToastMessage.success("Deleted Successfully")
            const remainingAssignments = assignments?.filter((assignment) => assignment.id !== id);
            setAssignments(remainingAssignments);
        } catch (error) {
            ToastMessage.error("An unexpected error occurred.", error);
            console.log("Thsi is error", error)
        }
    }

    return (
        <div className="container mt-4">
            <h2 className="text-center text-white mb-4">Assignments</h2>
            {assignments.length === 0 ? (
                <p className="text-center text-secondary">No assignments found.</p>
            ) : (
                <div className="row">
                    {assignments.map((assignment) => (
                            <Assignment
                                key={assignment.id}
                                title={assignment.title}
                                description={assignment.description}
                                submission_date={assignment.submission_date}
                                onAssignmentDelete={() => handleAssignmentDelete(assignment.id)}
                            />
                    ))}
                </div>
            )}
        </div>
    );
}
