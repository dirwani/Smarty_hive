import { useEffect, useState } from "react";
import { fetchAssignments, deleteAssignments } from "../../services/Forum/forum";
import ToastMessage from "../../utils/toaster/toaster";

export function Assignment() {
    const [assignments, setAssignments] = useState([]);
    const [isDeleting, setIsDeleting] = useState(false);

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
                        <div key={assignment.id} className="col-md-6 mb-4">
                            <div className="card bg-dark border-light h-100 shadow-sm text-white">
                                <div className="card-body">
                                    <h5 className="card-title text-warning">{assignment.title}</h5>
                                    <p className="card-text">{assignment.description}</p>
                                    <p className="card-text">
                                            Submission Date:{" "}
                                            {new Date(assignment.submission_date).toLocaleDateString()}
                                    </p>
                                    <button className="btn btn-danger" onClick={() => setIsDeleting(!isDeleting)}>Delete</button> 

                                    {isDeleting &&
                                        <div>
                                            <div>Do you want to delete?</div>
                                            <div className="btn btn-primary" onClick={() => setIsDeleting(!isDeleting)}>Cancel</div>
                                            <div className="btn btn-danger" onClick={handleAssignmentDelete(assignment.id)}>Confirm</div>
                                        </div>
                                    }

                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}
