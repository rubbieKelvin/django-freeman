import uuid
import typing
from .types import Pk
from .types import PartialUpdateType
from django.db import models, transaction
from freeman.utils.dsa import DotDict


class AbstractSharedModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        abstract = True

    def serialize(self) -> DotDict:
        """
        Turns a model into a JSON serializable data. Must be overridden by the subclass.

        Returns:
            DotDict: A dictionary representing the serialized data of the model.

        def serialize(self)-> DotDict:
            return DotDict({
                "date_created": self.date_created,
                "last_updated": self.last_updated
            })
        """
        raise NotImplementedError

    @classmethod
    def all(cls) -> models.manager.BaseManager[typing.Self]:
        """
        Retrieves all instances of the subclass.

        Returns:
            models.QuerySet: A queryset containing all instances of the subclass.
        """
        return cls.objects.all()

    @classmethod
    def findOneByPk(cls, pk: Pk) -> typing.Self:
        """
        Retrieves a single instance of the subclass by primary key.

        Args:
            pk (int | str): The primary key of the instance to retrieve.

        Raises:
            AbstractSharedModel.DoesNotExist: If no instance with the given primary key is found.

        Returns:
            AbstractSharedModel: An instance of the subclass with the given primary key.
        """

        return cls.all().get(pk=pk)

    @classmethod
    def findOneWhere(cls, where: models.Q) -> typing.Self:
        """
        Retrieves a single instance of the subclass that matches the given query.

        Args:
            where (models.Q): A query object that specifies the filtering conditions.

        Raises:
            AbstractSharedModel.DoesNotExist: If no instance is found that matches the given query.

        Returns:
            AbstractSharedModel: An instance of the subclass that matches the given query.
        """

        return cls.all().get(where)

    @classmethod
    def findMany(
        cls, where: models.Q, limit: int | None = None, page: int = 0
    ) -> models.manager.BaseManager[typing.Self]:
        """
        Retrieves multiple instances of the subclass that match the given query.

        Args:
            where (models.Q): A query object that specifies the filtering conditions.
            limit (int | None): The maximum number of instances to retrieve.
            page (int): The page to check on when using limits

        Returns:
            models.QuerySet: A queryset containing the instances of the subclass that match the given query.
        """

        res = cls.all().filter(where)
        if limit:
            offset = page * limit
            res = res[offset : offset + limit]
        return res

    @classmethod
    def insertSingle(
        cls, objectData: dict[str, typing.Any]
    ) -> typing.Self:
        """
        Inserts a single object into the database table.

        Args:
            objectData (dict[str, typing.Any]): A dictionary containing the data for the new object.

        Returns:
            AbstractSharedModel: The newly created instance of the subclass.
        """

        instance = cls.objects.create(**objectData)
        return instance

    @classmethod
    def insertMany(
        cls, objects: list[dict[str, typing.Any]]
    ) -> list[typing.Self]:
        """
        Inserts multiple objects into the database table.

        Args:
            objects (list[dict[str, typing.Any]]): A list of dictionaries, where each dictionary contains the data for an object.

        Returns:
            list[AbstractSharedModel]: A list of newly created instances of the subclass.
        """

        instances = [cls(**data) for data in objects]
        return cls.objects.bulk_create(instances)

    @classmethod
    def updateOne(cls, pk: Pk, _set: dict[str, typing.Any]) -> typing.Self:
        """
        Updates a single instance of the subclass that matches the given primary key with the specified fields.

        Args:
            pk (Pk): The primary key of the instance to update.
            _set (dict[str, typing.Any]): A dictionary containing the fields to update and their new values.

        Returns:
            AbstractSharedModel: The updated instance of the subclass.

        Raises:
            AbstractSharedModel.DoesNotExist: If no instance with the given primary key exists.
        """
        # Get the instance to update
        try:
            instance = cls.objects.get(pk=pk)
        except cls.DoesNotExist:
            raise AbstractSharedModel.DoesNotExist(
                f"No {cls.__name__} found with pk={pk}"
            )

        # Update the instance with the given set of fields
        for field, value in _set.items():
            setattr(instance, field, value)
        instance.save()

        return instance

    @classmethod
    def updateWhere(cls, where: models.Q, _set: dict[str, typing.Any]) -> int:
        """Updates all the objects with the _set that matches the where query. Returns the number of updated rows.

        Args:
            where (models.Q): The where clause to specify which objects to update.
            _set (dict): The dictionary of fields and values to update.

        Returns:
            int: The number of rows updated.
        """

        # Update all objects that match the where query with the given set of fields
        return cls.objects.filter(where).update(**_set)

    @classmethod
    def updateMany(cls, objects: list[PartialUpdateType]) -> list[typing.Self]:
        """Updates multiple objects with new values atomically. If one of the updates fail, all updates are rolled back.

        Args:
            objects (list[PartialUpdateType]): A list of dictionaries containing 'pk' and '_set' fields.

        Returns:
            list['AbstractSharedModel']: A list of the updated objects.
        """

        with transaction.atomic():
            updated_objects = []
            for obj in objects:
                pk = obj["pk"]
                _set = obj["_set"]
                try:
                    updated_object = cls.objects.filter(pk=pk).update(**_set)
                    updated_objects.append(updated_object)
                except Exception as e:
                    # Rollback the transaction if an update fails
                    transaction.set_rollback(True)
                    raise e
        return updated_objects

    @classmethod
    def deleteOne(cls, pk: Pk) -> None:
        """
        Deletes an instance of the subclass with the given primary key.

        Args:
            pk (Pk): The primary key of the instance to delete.

        Raises:
            AbstractSharedModel.DoesNotExist: If no instance with the given primary key exists.

        Returns:
            None
        """
        instance = cls.objects.get(pk=pk)
        instance.delete()

    @classmethod
    def deleteWhere(cls, where: models.Q) -> None:
        """
        Deletes all instances of the subclass that match the given query.

        Args:
            where (models.Q): A query object that specifies the filtering conditions.

        Returns:
            None.
        """
        cls.objects.filter(where).delete()
