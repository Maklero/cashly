import { faArrowRightFromBracket } from '@fortawesome/free-solid-svg-icons';

import { IconButton, Skeleton } from '@/components';
import { getLetterFromEmail } from '@/helpers/emailString';

import Tooltip from '../Tooltip/Tooltip';
import * as S from './CurrentUserDetails.styled';

export default function CurrentUserDetails({ user, logoutHandler, ...props }) {
  return user ? (
    <S.Container {...props}>
      <Tooltip text={user.email}>
        <S.UserAvatar letter={getLetterFromEmail(user.email)} />
      </Tooltip>
      <Tooltip text="Wyloguj się">
        <IconButton
          onClick={logoutHandler}
          variant="text"
          icon={faArrowRightFromBracket}
        />
      </Tooltip>
    </S.Container>
  ) : (
    <S.Container>
      <Skeleton
        type="circle"
        style={{ minWidth: '45px' }}
        width={45}
        height={45}
      />
      <Skeleton className="currentUserEmail" height={8} />
      <Skeleton style={{ minWidth: 40 }} width={40} height={40} />
    </S.Container>
  );
}
