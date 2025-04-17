
import { useState } from "react";

export default function Assignment({title,description,submission_date,onAssignmentDelete}){
    const [isDeleting, setIsDeleting] = useState(false);


    return (
        <>
        <div className="col-md-6 mb-4">
            <div className="card bg-dark border-light h-100 shadow-sm text-white">
                <div className="card-body">
                    <h5 className="card-title text-warning">{title}</h5>
                    <p className="card-text">{description}</p>
                    <p className="card-text">
                            Submission Date:{" "}
                            {new Date(submission_date).toLocaleDateString()}
                    </p>
                    <button className="btn btn-danger" onClick={() => setIsDeleting(!isDeleting)}>Delete</button> 

                    {isDeleting &&
                        <div>
                            <div>Do you want to delete?</div>
                            <div className="btn btn-primary" onClick={() => setIsDeleting(!isDeleting)}>Cancel</div>
                            <div className="btn btn-danger" onClick={onAssignmentDelete}>Confirm</div>
                        </div>
                    }

                </div>
            </div>
        </div>
        </>
    )
}