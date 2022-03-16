from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database_handler import get_db
from .. import pydantic_model, models, oauth2

# Router instance
router = APIRouter(prefix="/love", tags=['Love'])

@router.post("/", status_code=status.HTTP_201_CREATED)
def love(love: pydantic_model.Love, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # If one love aready given
    # Check if it is valid to give more
    # But, to check this
    # It must have the same post id and it must check if it already has the current user
    # if yes don't give any love vote
    love_query = db.query(models.Love).filter(models.Love.post_id == love.post_id, models.Love.user_id == current_user.id)
    found_love = love_query.first()

    # If already found love
    if(love.dir == 1):

        if found_love:
            raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail=f"User with id: {current_user.id} has alredy loved this post with id: {love.post_id}")

        # Save the new love with post id and the current user's id
        new_love = models.Love(post_id = love.post_id, user_id = current_user.id)

        # Add it and commit it to the database
        db.add(new_love)
        db.commit()

        # Return to the user a simple message
        return{"message": "You have loved this post"}

    # Otherwise the user wants to undo the love
    else:

        # But before if not found
        if not found_love:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This post has no loves")

        # But if found let's
        love_query.delete(synchronize_session = False)
        db.commit()

        return{"message": "You have unloved this post"}
